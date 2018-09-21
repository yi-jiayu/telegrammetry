# tgrm
A Telegram relationship manager which shows you a dashboard of your Telegram activity.

![tgrm dashboard](https://user-images.githubusercontent.com/11734309/45871491-3841b180-bdc0-11e8-84d4-a8b29a51c5ea.png)

## Dependencies
- Python (tested with 3.7)
- Elasticsearch (tested with 6.2.4)
- Kibana (tested with 6.2.4)
- Filebeat (tested with 6.2.4)

## Setup
1. Fill in your Telegram account details into `telegram.ini`.

2. Run `messages.py` and redirect its output to a file:
```
PYTHONUNBUFFERED=1 python messages.py > messages.log
```
Note: You need to run `messages.py` at least once first to set up your Telegram session on a new device with the code that will be sent to you.

3. Start Elasticsearch

4. Modify `filebeat.yml` and add your message log path under `paths` for the log input:
```
 # Paths that should be crawled and fetched. Glob based paths.
  paths:
    - /path/to/your/log/file
```

5. Start Filebeat and set the config path to the `tgrm` folder:
```
filebeat -e --path.config $PWD
```
The `-e` flag tells Filebeat to log to standard error.

6. Start Kibana.

7. Inside Kibana, create an index pattern for `filebeat-`, selecting `timestamp` as the Time Filter field name.

8. After creating a new index pattern, go to the "Management" tab and select "Index Patterns". The ID of the newly-created index pattern will be in the address bar just behind `indices/`. Copy it.

9. Inside `visualisations.json`, replace all IDs under `kibanaSavedObjectMeta.searchSourceJSON.index` with your index ID.

10. Go to "Saved Objects" under the "Management" tab and import your modified `visualisations.json` and `dashboard.json`.
