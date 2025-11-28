# Personal AWS Support Agent

AWS の一般的な質問や GenU をはじめとしたソリューションの基本的な使い方をいつでも説明してくれる **あなただけの** エージェントです。

## 含まれているナレッジ

- **AWS General** - 一般的な AWS の質問と Bedrock FAQ
- **GenU Documentation** - Generative AI Use Cases アプリケーションの完全ガイド

## クイックスタート

ワンクリックで Personal Support Agent をデプロイできます

| リージョン | Launch Stack |
|-----------|--------------|
| 東京 (ap-northeast-1) | [![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://ap-northeast-1.console.aws.amazon.com/cloudformation/home#/stacks/create/review?stackName=PersonalSupportAgentStack&templateURL=https://aws-ml-jp.s3.ap-northeast-1.amazonaws.com/asset-deployments/agents/PersonalSupportAgentDeploymentStack.yaml){target="_blank"} |
| バージニア北部 (us-east-1) | [![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://us-east-1.console.aws.amazon.com/cloudformation/home#/stacks/create/review?stackName=PersonalSupportAgentStack&templateURL=https://aws-ml-jp.s3.ap-northeast-1.amazonaws.com/asset-deployments/agents/PersonalSupportAgentDeploymentStack.yaml){target="_blank"} |
| オレゴン (us-west-2) | [![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://us-west-2.console.aws.amazon.com/cloudformation/home#/stacks/create/review?stackName=PersonalSupportAgentStack&templateURL=https://aws-ml-jp.s3.ap-northeast-1.amazonaws.com/asset-deployments/agents/PersonalSupportAgentDeploymentStack.yaml){target="_blank"} |


### GenU との連携

[GenU のワンクリックデプロイ](https://aws-samples.github.io/sample-one-click-generative-ai-solutions/) では、こちらのエージェントがデプロイされていると "AgentCore" で使えるエージェントとして自動的に組み込んでくれます。

![image](assets/images/genu_integration.png)

* Integration/GenU のタグがつけられた Stack でデプロイされた Agent を読み込むようにしています。詳細は[ワンクリックデプロイの GenU ページ](https://aws-samples.github.io/sample-one-click-generative-ai-solutions/solutions/generative-ai-use-cases/)を参照ください。

## リポジトリ

[GitHub Repository](https://github.com/icoxfog417/personal-account-manager)
