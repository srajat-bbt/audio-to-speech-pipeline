MAX_LOAD_DATE_FOR_MEDIA_QUERY = "SELECT MAX (load_datetime) FROM media;"
INSERT_INTO_MEDIA_TABLE_QUERY = "INSERT INTO media(audio_id,raw_file_name,total_duration,title,cleaned_duration,num_of_speakers,\
        language,has_other_audio_signature,type,source,source_url,source_website,utterances_files_list,recorded_state,\
            recorded_district,recorded_place,recorded_date,purpose,load_datetime) SELECT audio_id,raw_file_name,duration,\
                title,cleaned_duration,num_of_speakers,language,has_other_audio_signature,type,source,source_url,source_website,\
                utterances_files_list,recorded_state,recorded_district,recorded_place,recorded_date,purpose,load_datetime FROM media_metadata_staging where load_datetime > :max_datetime;"

GET_SPEAKER_ID_QUERY = "select speaker_id from speaker s JOIN media_metadata_staging b on s.speaker_name = b.speaker_name \
            where b.audio_id = :audio_id;"

GET_LOAD_TIME_FOR_AUDIO_QUERY = "select load_datetime from media where audio_id = :audio_id;"

FIND_MAX_LOAD_DATE_QUERY = "SELECT MAX(load_datetime) FROM media_speaker_mapping;"

GET_AUDIO_ID_QUERY = "SELECT media.audio_id FROM media where load_datetime > :max_load_date"

INSERT_UNIQUE_SPEAKER_QUERY = "INSERT INTO speaker(speaker_name,source,gender,mother_tongue,age_group,load_datetime) SELECT t.speaker_name,\
    t.source,min(speaker_gender),min(t.mother_tongue),min(t.age_group),min(t.load_datetime) \
        FROM media_metadata_staging t LEFT JOIN speaker ts ON ts.speaker_name = t.speaker_name WHERE ts.speaker_name IS NULL group by t.speaker_name, t.source"
