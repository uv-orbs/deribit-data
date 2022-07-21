#gcloud compute ssh --zone "us-central1-a" "influx-2"  --project "stunning-choir-314214"
gcloud compute scp main.py influx-2:~/derinit-data --zone="us-central1-a" --project "stunning-choir-314214" 
gcloud compute scp --recursive .venv/ influx-2:~/derinit-data/.venv/* --zone="us-central1-a" --project "stunning-choir-314214" 