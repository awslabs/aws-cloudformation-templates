# String functions

Provides string transformation utility functions.

## Basic Usage

Place the transform where you would like the output to be placed and provide the input string as the value for the
InputString Parameter. The example below shows converting an input parameter to upper case and setting it as the value
for a tag on an s3 bucket.

```yaml
Parameters:
  InputString:
    Default: "This is a test input string"
    Type: String
Resources:
  S3Bucket:
    Type: "AWS::S3::Bucket"
    Properties:
      Tags:
        - Key: Upper
          Value:
            Fn::Transform:
              Name: 'String'
              Parameters:
                InputString: !Ref InputString
                Operation: Upper
```

## Available Operations

### Upper

Return a copy of the string with all the cased characters converted to uppercase.

### Lower

Return a copy of the string with all the cased characters [4] converted to lowercase.

### Capitalize

Return a copy of the string with its first character capitalized and the rest lowercased.

### Title

Return a titlecased version of the string where words start with an uppercase character and the remaining characters
are lowercase.

### SwapCase

Return a copy of the string with uppercase characters converted to lowercase and vice versa.

### Strip

Return a copy of the string with the leading and trailing characters removed. The `Chars` parameter is a string
specifying the set of characters to be removed. If omitted default is to remove whitespace. The Chars argument is not a
prefix or suffix; rather, all combinations of its values are stripped.

#### Additional Parameters

*Chars*: [optional] characters to strip from beginning and end of string

### Replace

Return a copy of the string with all occurrences of substring `Old` replaced by `New`.

#### Additional Parameters

*Old*: [required] sub-string to search for

*New*: [required] string to replace Old with

### MaxLength

Return a copy of the string with a maximum length as specified by the `Length` parameter. Default is to strip
characters from the end of the string.

#### Additional Parameters

*Length*: [required] maximum length of string

*StripFrom*: [optional] specifying `Left` will strip characters from the beginning of the string, `Right` from the end
(default)

## Author

[Jay McConnell](https://github.com/jaymccon)  
Partner Solutions Architect  
Amazon Web Services
