# DatetimeNow functions

Provides the current datetime as a formatted string.

## Basic Usage

Place the transform where you would like the output to be placed and provide the string format as the value for the
`format` Parameter. The macro uses Python so the supported format codes match those used by the python `strftime` method.
A Full list of supported codes can be found [here](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

The example below shows retrieving the current date time as a string in the format 'YYYY-MM-DD hh:mm:ss' and setting it as the value
for a tag on an s3 bucket.

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
        - Key: DatetimeNow
          Value:
            'Fn::Transform':
             - Name: 'DatetimeNow'
               Parameters:
                 format: '%Y-%m-%d %H:%M:%S'
```

## Author

[Dan Johns](https://github.com/danjhd)
Senior SA Engineer
Amazon Web Services
