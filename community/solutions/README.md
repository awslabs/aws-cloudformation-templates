# Introduction
Create CodePipeline by separating CodeCommit & CodePipeline under its own Account.

# PreRequisites
  #### 1. At least 2 separate AWS Accounts
        - Account A => One Account holding an existing CodeCommit Repository
        - Account B => Where CodePipeline will be created
  #### 2. Beanstalk Application hosted in `Account B`

# Installation Steps
1. Deploy `codecommit.yaml` into `Account A`. Make sure to leave `CMKARN` Parameter blank.
2. Deploy `codepipeline.yaml` into `Account B`. All Parameters are compulsory.
3. Update `CodeCommit` Stack (deployed in #1) by adding `CMKARN` Parameter (from `CodePipeline` CFN output in #2)
4. Deploy changes by releasing changes in CodePipeline Console.
