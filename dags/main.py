from airflow import DAG # type: ignore
import pendulum # type: ignore
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_ids, extract_video_date, save_to_json
from datawarehouse.dwh import staging_table, core_table

#Local timezone

local_tz = pendulum.timezone("America/Bogota")

default_args ={
    "owner":"dataengineer",
    "depends_on_past":False,
    "email_on_failure":False,
    "email_on_retry":False,
    "email":"alej2498@gmail.com",
    #"retries":1,
    #retry_delay:timedelta(minutes=5),
    "max_active_runs":1,
    "dagrun_timeout":timedelta(hours=1),
    "start_date": datetime(2026,10,15, tzinfo=local_tz),
    #"end_date":datetime(2026,10,30, tzinfo=local_tz),
}

with DAG(
    dag_id = "produce_json",
    default_args = default_args,
    description = "DAG to produce JSON file with raw data",
    schedule = "0 14 * * *",  #Ejecuta a las 14 horas
    catchup = False, #No se pone al dia con dag perdidos
) as dag:

    #Define task
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_date(video_ids)
    save_to_json_task = save_to_json(extract_data)

    #Define dependencias
    playlist_id >> video_ids >> extract_data >> save_to_json_task



with DAG(
    dag_id = "update_db",
    default_args = default_args,
    description = "DAG to process json file and insert data bioth staging and core schemas",
    schedule = "0 15 * * *",  #Ejecuta a las 14 horas
    catchup = False, #No se pone al dia con dag perdidos
) as dag:

    #Define task
    update_staging = staging_table()
    update_core = core_table()
 
    #Define dependencias
    update_staging >> update_core 