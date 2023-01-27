

class JobQueueService():

    # { job_type: [some_function], args: {process_model_identifier: [identifier], type: [cycle or datetime], start: [datetime],
    #   duration: [int - cycle only], cycles: [int - cycle only] }}
    def consume_message_from_job_queue():
