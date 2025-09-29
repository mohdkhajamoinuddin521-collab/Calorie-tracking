set -o errexit  # Exit on error

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate # Apply database migrations

# if [[$CREATE_SUPERUSER]];
# then
#     python manage.py createsuperuser --noinput
# fi

