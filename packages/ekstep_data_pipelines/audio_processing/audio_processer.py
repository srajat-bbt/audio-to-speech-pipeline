import os
from audio_processing.constants import CONFIG_NAME, REMOTE_RAW_FILE, CHUNKING_CONFIG
from common.utils import get_logger

Logger = get_logger("Audio Processor")


class AudioProcessor:

    """
    Class for breaking a downloaded file into smaller chunks of
    audio files as well as filtering out files with more than an acceptable level
    of Sound to Noise Ratio(or SNR)
    """

    DEFAULT_DOWNLOAD_PATH = '/tmp/audio_processing_raw'

    @staticmethod
    def get_instance(data_processor, gcs_instance, audio_commons):
        return AudioProcessor(data_processor, gcs_instance, audio_commons)

    def __init__(self, data_processor, gcs_instance, audio_commons):
        self.data_processor = data_processor
        self.gcs_instance = gcs_instance
        self.snr_processor = audio_commons.get('snr_util')
        self.chunking_processor = audio_commons.get('chunking_conversion')
        self.audio_processor_config = None


    def process(self, **kwargs):
        """
        Function for breaking an audio file into smaller chunks and then
        accepting/rejecting them basis the SNR ratio.
        """
        self.audio_processor_config = self.data_processor.config_dict.get(
            CONFIG_NAME)

        audio_id_list = kwargs.get('audio_id_list', [])
        source = kwargs.get('source')
        extension = kwargs.get('extension')

        Logger.info(f'Processing audio ids {audio_id_list}')
        for audio_id in audio_id_list:
            Logger.info(f'Processing audio_id {audio_id}')
            self.process_audio_id(audio_id, source, extension)


    def process_audio_id(self, audio_id, source, extension):

        local_audio_download_path = f'{AudioProcessor.DEFAULT_DOWNLOAD_PATH}/{source}/{audio_id}'

        Logger.info(f'Downloading file for audio_id/{audio_id} to {local_audio_download_path}')

        self.ensure_path(local_audio_download_path)
        Logger.info(f'Ensured {local_audio_download_path} exists')

        remote_file_path = self.audio_processor_config.get(REMOTE_RAW_FILE)
        remote_download_path = f'{remote_file_path}/{source}/{audio_id}'

        Logger.info(f'Downloading audio file from {remote_download_path} to {local_audio_download_path}')
        self.gcs_instance.download_to_local(self.gcs_instance.bucket, remote_download_path,
                                            local_audio_download_path, True)

        Logger.info(f'Conerting the file with audio_id {audio_id} to wav')
        local_converted_wav_file_path = self._convert_to_wav(local_audio_download_path, extension)

        Logger.info(f'Breaking {audio_id} at {local_converted_wav_file_path} file into chunks')
        chunk_output_path, vad_output_path = self._break_files_into_chunks(audio_id, local_audio_download_path, local_converted_wav_file_path)

        self._process_snr()

    def ensure_path(self, path):
        # TODO: make path empty before creating it again
        os.makedirs(path, exist_ok=True)

    def _convert_to_wav(self, source_file_directory, extension):
        Logger.info(f'Converting the contents of the local path {source_file_directory} to wav')

        local_output_directory = f'{source_file_directory}/wav'

        self.ensure_path(local_output_directory)
        Logger.info(f'Output initialized to local path {local_output_directory}')

        return self.chunking_processor.convert_to_wav(source_file_directory, output_dir=local_output_directory, ext=extension)



    def _break_files_into_chunks(self, audio_id, local_download_path, wav_file_path):

        Logger.info(f'Chunking audio file at {wav_file_path}')
        local_chunk_output_path = f'{local_download_path}/chunks'
        local_vad_output_path = f'{local_download_path}/vad'

        aggressivness_dict = self.audio_processor_config.get(CHUNKING_CONFIG, {'aggressiveness':2})

        if not isinstance(aggressivness_dict.get('aggressiveness'), int):
            raise Exception(f'Aggressiveness must be an int, not {aggressivness_dict}')

        self.ensure_path(local_chunk_output_path)
        Logger.info(f'Ensuring path {local_chunk_output_path}')
        file_name = wav_file_path.split('/')[-1]

        self.chunking_processor.create_audio_clips(aggressivness_dict.get('aggressiveness'), wav_file_path, local_chunk_output_path, local_vad_output_path, file_name)

        return local_chunk_output_path, local_vad_output_path



    def _process_snr(self):
        pass
