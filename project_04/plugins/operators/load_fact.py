from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 query="",
                 truncate_table=False,                
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table=table
        self.query=query
        self.truncate_table=truncate_table

    def execute(self, context):
        self.log.info(f'Query: {self.query}')    
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.truncate_table:
            self.log.info(f'Truncating table before insertion')
            redshift.run(f"TRUNCATE TABLE {self.table}")
        self.log.info(f'Inserting data into table ...') 
        redshift.run(f"INSERT INTO {self.table} {self.query}")