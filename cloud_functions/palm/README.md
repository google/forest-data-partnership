# Palm Conversion Risk Cloud Function

**EXPERIMENTAL!!**

For the Forest Data Partnership, we have developed a Cloud Function that
calculates the risk of palm transitions in forest categories.

The function takes in a GeoJSON geometry representing a region of interest, and
returns information about palm transition risk in that region, in forest and
non-forest areas (according to
[this dataset](https://developers.google.com/earth-engine/datasets/catalog/JRC_GFC2020_V1?hl=en#description)).
The function uses Earth Engine to do the geospatial analysis, and uses the palm
model described here:
[A community palm model](https://goo.gle/a_community_palm_model).

The source code for the Cloud Function can be found in this directory.

## Setting up the Cloud Function

To deploy the Cloud Function in your own Cloud Project, you must have sufficient
permissions on the project, the project must be registered to use Earth Engine
([reference](https://developers.google.com/earth-engine/cloud/earthengine_cloud_project_setup#get-access-to-earth-engine))
and the project must have the Earth Engine API enabled.

### Configuration

1.  Follow the “Before you begin” quickstart setup instructions:
    https://cloud.google.com/functions/docs/console-quickstart.
2.  Go to the Cloud Functions page in the Google Cloud console:
    https://console.cloud.google.com/functions.
3.  Click CREATE FUNCTION. Under Basics, leave environment as 2nd gen and name
    your function. The name will be part of the URL.
4.  Select a region. Leave Trigger as is (HTTPS trigger, require
    authentication).
5.  Leave other settings as is.
6.  Click NEXT.

### Code

1.  Change the runtime to Python 3.12.
2.  Change the entry point to `main`. This is the name of the function that will
    be called by the Cloud Function.
3.  Update the code to match the code in this directory.
4.  Ensure the `requirements.txt` file contains: \
    `functions-framework==3.* earthengine-api>=0.1.200`
5.  Click DEPLOY!

## Calling the Cloud Function

After deploying the Cloud Function, it can be called directly through `curl`.
The `gcloud auth` command is used for authentication and authorization.

The request format requires a region parameter, which is the GeoJSON of the
geometry to calculate forest conversion risk for.

The output is a list of two elements. The elements represent non-forest and
forest palm conversion risks.

Example request:

```
curl -X POST https://us-central1-forest-data-partnership.cloudfunctions.net/palm_transitions \
-H "Authorization: bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json" \
-d '{
  "region":
{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[115.70711519531247,-3.3387465908503833],[115.7241955023193,-3.3387465908503833],[115.7241955023193,-3.324694149698577],[115.70711519531247,-3.324694149698577],[115.70711519531247,-3.3387465908503833]]]}}
}'
```

Example response:

```
[{"Area (ha)": 4.646123412041769, "Area from palm (ha)": 0.6283549765350778, "Area to palm (ha)": 0.403191217913683, "forest": 0}, {"Area (ha)": 290.3170576655356, "Area from palm (ha)": 33.78877207904208, "Area to palm (ha)": 27.100131561812102, "forest": 1}]
```

### Permissions

To allow users to call the Cloud Function, the caller must have the Cloud Run
Invoker role. To set this up, go to Cloud Run > Services, select the service
that corresponds to the cloud function, click Permissions and Add Principal,
then give the user the Cloud Run Invoker role
([reference](https://cloud.google.com/functions/docs/securing/authenticating#auth-func-to-func)).
