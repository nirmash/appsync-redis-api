# Add a Serverless front-end to your ElastiCache Redis cluster

This repo includes a SAM template and Lambda function that setup an AppSync API in-front of an Amazon [ElastiCache for Redis](https://aws.amazon.com/elasticache/redis/) cluster.

![architecture](https://raw.githubusercontent.com/nirmash/appsync-redis-api/master/AppSyncBlog.jpg?token=AAKPFPWY4CMRQ6BYT4G2NAK7JXPSE)

## Requirements

* AWS CLI [installed](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and configured with Administrator permission
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3.8.x](https://www.python.org/downloads/) - is not required to run the sample but will be needed to make changes

## Setup process

Clone this git repo locally and go to the project directory
```shell
$ git clone https://github.com/nirmash/appsync-redis-api.git
Cloning into 'appsync-redis-api'...
remote: Enumerating objects: 39, done.
remote: Counting objects: 100% (39/39), done.
remote: Compressing objects: 100% (20/20), done.
remote: Total 39 (delta 19), reused 37 (delta 17), pack-reused 0
Unpacking objects: 100% (39/39), done.
$ cd appsync-redis-api/
```
Build the SAM deployment package 
```shell'
$ sam build
Building function 'RedisExecuteCommand'
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource

Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Invoke Function: sam local invoke
[*] Deploy: sam deploy --guided
```
Deploy the application. 
**Note:** The SAM template will create a new AppSync API, a Lambda Function and an Amazon ElastiCache cluster.
```shell
$ sam deploy --guided
```
When prompted, select a stack name (the name of the CloudFormation stack that you will use to delete the application later). Your preferred AWS Region and the name for the AppSync API to be created. 
**Note:** You will need the AppSync API name later to obtain the API ID. 

```shell
Configuring SAM deploy
======================

	Looking for samconfig.toml :  Not found

	Setting default arguments for 'sam deploy'
	=========================================
	Stack Name [sam-app]: redisAppSyncApi
	AWS Region [us-east-1]: us-west-2
	Parameter RedisGraphQLApiName [Redis-GraphQL-Api]: RedisAppSyncApi
```
Follow the rest of the prompts. SAM will create a CloudFormation template and deploy the application components, this will take a few minutes.
```shell
    ... Deployment status will show here ... 

    CloudFormation outputs from deployed stack
    -------------------------------------------------------------------------------------------------------------
    Outputs
    -------------------------------------------------------------------------------------------------------------
    Key                 RedisExecuteCommand
    Description         -
    Value               arn:aws:lambda:us-west-2:000000000000:function:redisAppSyncApi-RedisExecuteCommand-
    HHPLVD8UHTH3

    Key                 RedisQueryAPI
    Description         -
    Value               arn:aws:appsync:us-west-2:00000000000:apis/xxxxxxxxxxxxxxx
    -------------------------------------------------------------------------------------------------------------
$
```
## Validating and testing
Once the deployment is completed you will see the below output. We will then obtain the API Key for the App Sync API and execute some Redis commands against it. 
To obtain the API Key you will need the API Id. You will do that by calling the aws cli.
```shell
$ aws appsync list-graphql-apis
```
Copy the `"apiId"` from the command output. To obtain the API Key, call another aws cli command. Also, copy the value of the `"GRAPHQL"` uri endpoint for later use.

```shell
$ aws appsync list-api-keys --api-id <your api Id>
```
Copy the `"id"` value from the command output. You now have what you need to test your new API. 
The image below shows the steps in a terminal window. 

![terminal window](https://raw.githubusercontent.com/nirmash/appsync-redis-api/master/cli-api-ids.jpg?token=AAKPFPTCER3H3LXFSH2K7FS7J7LBY)

To make testing easier this repo includes a simple HTML test client that attempts to emulate the redis-cli. To get it to work, just double-click the `index.html` file in the root directory of the repo. Paste the GraphQL uri endpoint and API key you saved earlier into the HTML form and hit the connect button, once connected, `>>` will appear in the cli text area. You can now use some Redis commands to communicate with ElastiCache for Redis!

![cli client](https://raw.githubusercontent.com/nirmash/appsync-redis-api/master/redisHTMLClient.jpg?token=AAKPFPQDXOBF7QRZKHYDG227J6ZY2)

## Clean-up
You can use the AWS cloud formation CLI to remove the cloud components you deployed with SAM. 
```shell
aws cloudformation delete-stack --stack-name <Stack Name you entered earlier>
```
**Note:** This call is asynchronous so don’t be alarmed when it completes immediately. You can check the AWS Console CloudFormation screen for the stack deletion status. 
