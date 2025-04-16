import boto3

# Step 1: Get the MediaConvert endpoint (only need to do this once)
mc_client = boto3.client("mediaconvert", region_name="ap-southeast-1")
endpoints = mc_client.describe_endpoints()
endpoint_url = endpoints["Endpoints"][0]["Url"]

# Step 2: Create the actual MediaConvert client with the custom endpoint
mediaconvert = boto3.client(
    "mediaconvert", region_name="ap-southeast-1", endpoint_url=endpoint_url
)

# Step 3: Create a job to merge video and audio
job = mediaconvert.create_job(
    Role="arn:aws:iam::YOUR_ACCOUNT_ID:role/MediaConvert_Default_Role",
    Settings={
        "Inputs": [
            {
                "AudioSelectors": {
                    "Audio Selector 1": {"DefaultSelection": "DEFAULT", "Tracks": [1]}
                },
                "VideoSelector": {},
                "TimecodeSource": "ZEROBASED",
                "FileInput": "s3://your-bucket/inputs/minecraft1.mp4",
            },
            {
                "AudioSelectors": {
                    "Audio Selector 1": {"DefaultSelection": "DEFAULT", "Tracks": [1]}
                },
                "VideoSelector": {"ColorSpace": "FOLLOW"},
                "TimecodeSource": "ZEROBASED",
                "FileInput": "s3://your-bucket/inputs/raw.mp3",
            },
        ],
        "OutputGroups": [
            {
                "Name": "File Group",
                "OutputGroupSettings": {
                    "Type": "FILE_GROUP_SETTINGS",
                    "FileGroupSettings": {"Destination": "s3://your-bucket/outputs/"},
                },
                "Outputs": [
                    {
                        "ContainerSettings": {"Container": "MP4"},
                        "VideoDescription": {"CodecSettings": {"Codec": "H_264"}},
                        "AudioDescriptions": [
                            {
                                "AudioSourceName": "Audio Selector 1",
                                "CodecSettings": {"Codec": "AAC"},
                            }
                        ],
                    }
                ],
            }
        ],
    },
)

print(f"MediaConvert Job Created: {job['Job']['Id']}")
