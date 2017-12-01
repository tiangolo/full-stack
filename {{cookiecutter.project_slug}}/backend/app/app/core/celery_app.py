from celery import Celery

celery_app = Celery('worker', broker='amqp://guest@queue//')

celery_app.conf.task_routes = {
    'main.worker.test_task': 'main-queue',
}
