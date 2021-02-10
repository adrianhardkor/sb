node() {
    def os = System.properties['os.name'].toLowerCase()
    try {
        notifyBuild('STARTED')
        def passthruString = sh(script: "printenv", returnStdout: true)
        passthruString = passthruString.replaceAll('\n',' ').trim()
        def paramsString1 = params.toString().replaceAll("[\\[\\](){}]","")
        paramsString = paramsString1.replaceAll(', ',' ')
        def paramsStringXray = formatXray(paramsString1, ', ')
        def HUDSON_URL = "${env.HUDSON_URL}"
        def SERVER_JENKINS = ""
        if (HUDSON_URL.contains("10.88.48.21")) {
            SERVER_JENKINS = "WOPR-SB"
        } else {
            SERVER_JENKINS = "WOPR-PROD-JENKINS"
        }
        stage("Prepare Workspace") {
            echo "*** Prepare Workspace ***"
            cleanWs()
            // sh "ls -l"
            env.WORKSPACE_LOCAL = sh(returnStdout: true, script: 'pwd').trim()
            env.BUILD_TIME = "${BUILD_TIMESTAMP}"
            echo "Workspace set to:" + env.WORKSPACE_LOCAL
            echo "Build time:" + env.BUILD_TIME
        }
        stage('Checkout Self') {
            echo "\n\n GIT ENTIRE REPO"
            checkout scm
            // sh "ls -l"
        }
        stage('Checkout shared_libs') {
            echo " ** REPO SHARED LIBRARIES FOR ALL GIT-ARC PROJECTS ** "
            sh """
                mkdir lib
                cd lib/
                git clone ${GIT_SHARED_LIB}
                cd ..
                ls -l ./lib/shared_libs/
            """
            echo "\n\n"
        }
    }
    catch(e) {
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        throw e
    } finally {
        // Success or failure, always send notifications
        echo "I AM HERE"
        notifyBuild(currentBuild.result)
        sendEmail(currentBuild.result)
    }
}
def formatXray(input_string, String delimiter = "\n") {
    result = ""
    for(line in input_string.split(delimiter)) {
        result = result.replaceAll("\t","    ") + "\\n" + line
        // single to double / for all
    }
    return result
}
def notifyBuild(String buildStatus = 'STARTED') {
    // build status of null means successful
    buildStatus =  buildStatus ?: 'SUCCESSFUL'
    // Default values
    def colorName = 'RED'
    def colorCode = '#FF0000'
    def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
    def summary = "${subject} (${env.BUILD_URL})"
    def details = """<p>STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
      <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""
      // Override default values based on build status
      if (buildStatus == 'STARTED') {
        color = 'BLUE'
        colorCode = '#0000FF'
        msg = "Build: ${env.JOB_NAME} has started: ${BUILD_TIMESTAMP}"
      } else if (buildStatus == 'UNSTABLE') {
        color = 'YELLOW'
        colorCode = '#FFFF00'
        msg = "Build: ${env.JOB_NAME} was listed as unstable. Look at ${env.BUILD_URL} and Report: ${env.BUILD_URL}/cucumber-html-reports/overview-features.html"
      } else if (buildStatus == 'SUCCESSFUL') {
        color = 'GREEN'
        colorCode = '#00FF00'
        msg = "Build: ${env.JOB_NAME} Completed Successfully ${env.BUILD_URL} Report: ${env.BUILD_URL}/cucumber-html-reports/overview-features.html"
      } else {
        color = 'RED'
        colorCode = '#FF0000'
        msg = "Build: ${env.JOB_NAME} had an issue ${env.BUILD_URL}/console"
      }
    // Send notifications
    slackSend baseUrl: 'https://hooks.slack.com/services/', 
    channel: 'wopr-jenkins-test', 
    color: colorCode, 
    message: msg,
    teamDomain: 'https://wow-technology.slack.com', 
    tokenCredentialId: 'Slack-Token', 
    username: 'JenkinsAutomation'
}
def sendEmail(String buildStatus = 'STARTED') {
    // build status of null means successful
    // if buildStatus is not STARTED and mailRecipients is a parameter
    buildStatus =  buildStatus ?: 'SUCCESSFUL'
    if (buildStatus != 'STARTED') {
        if (params.toString().contains("mailRecipients")) {
            def jobName = currentBuild.fullDisplayName
            emailext body: '''${SCRIPT, template="groovy-html.template"}''',
                mimeType: 'text/html',
                subject: "[Jenkins] ${jobName}",
                to: "${params.mailRecipients}",
                replyTo: "${params.mailRecipients}",
                recipientProviders: [[$class: 'CulpritsRecipientProvider']]
        }
    }
}
