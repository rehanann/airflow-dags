from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(  # ← Assign DAG to variable so Airflow can detect it
    dag_id='deploy_spark_chart_bashoperator',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['helm', 'spark'],
)

deploy_chart = BashOperator(
    task_id='deploy_spark_chart',
    bash_command="""
    curl -X POST \
      http://helm-api-api.default.svc.cluster.local:8000/install \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
        "release_name": "mytest",
        "chart_name": "spark-chart/spark-chart",
        "namespace": "test",
        "values": {
          "additionalProp1": {}
        }
      }'
    """,
    dag=dag,  # ← Ensure task is bound to DAG
)
