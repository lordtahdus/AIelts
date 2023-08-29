import os
import openai
from decouple import config


"""
export OPENAI_API_KEY='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'

To upload file:
curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "purpose=fine-tune" \
  -F "file=@C:\Users\ADMIN\Documents\GitHub\AIelts\fine_tuning\tr\train_tr_sample.jsonl"


To create finetune:
curl https://api.openai.com/v1/fine_tuning/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "training_file": "file-FDTmsxE8E4LkJFKUwQ01f2mj",
    "model": "babbage-002",
    "suffix": "tr_test_2908"
  }'

Retrieve finetune:
curl https://api.openai.com/v1/fine_tuning/jobs/ftjob-jMDrLwaXLtlx8okVCUWW8gAy \
  -H "Authorization: Bearer $OPENAI_API_KEY"

List finetune events:
curl https://api.openai.com/v1/fine_tuning/jobs/ftjob-jMDrLwaXLtlx8okVCUWW8gAy/events \
  -H "Authorization: Bearer $OPENAI_API_KEY"
"""

def create_finetune():
    openai.FineTuningJob.create(
        training_file = "file-CKhRhLM3jyoc8EEQS6cB6eju", 
        model = "babbage-002", # "gpt-3.5-turbo"
        suffix = "cc_test_2908"
    )
    # THIS NOT WORKING



if __name__ == "__main__":
    openai.api_key = config('OPENAI_KEY_1')

    # THE SHIT BELOW NOT WORKING
    # create_finetune()
    openai.File.list() 
    openai.FineTuningJob.list(limit=10)