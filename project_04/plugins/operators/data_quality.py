from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.checks = checks

    def execute(self, context):
        self.log.info('Checking data quality ...')
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        for check in checks:
            query = check['query']
            expected_result = check['expected_result']
            
            data = redshift_hook.get_records(query)
            
            if data[0][0] != expected_result:
                raise ValueError(f'Data quality check failed!'
            self.log.info('All data quality checks passed!')
        
        
        
        