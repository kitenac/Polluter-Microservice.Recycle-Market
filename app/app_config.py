APP_WORK_CFG = {
    'WORK_MODE': 'dev',  # dev / prod - affects DB
    'db-hosts': {
        'dev': '127.0.0.1',           # for development
        'prod': 'Postgres_4_Polluter_Service'   # when backend run as container | note: Docker`s internal DNS would resolve container`s ip by name of container
    },
    'db-name': 'Polluter-Service',
    'service-name': 'Polluter-Service',
}