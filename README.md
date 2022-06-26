# Django docker template

A template for a bare-bone django app for quick development.

To start the app:

```shell
docker-compose up
```

After model changes:
```Ctrl-C``` the above command and re-run it. 
This will automatically apply and model changes by running the makemigrations and migrate commands before startup.
