node() {

    def repoURL = "https://github.com/adrianhardkor/sb.git"

    def STC_INSTALL = "/opt/STC_CLIENT/Spirent_TestCenter_5.16/Spirent_TestCenter_Application_Linux64Client/"
    def os = System.properties['os.name'].toLowerCase()

    stage("Prepare Workspace") {
        echo "*** Prepare Workspace ***"
        cleanWs()
        env.WORKSPACE_LOCAL = sh(returnStdout: true, script: 'pwd').trim()
        passthruString = sh(script: "printenv", returnStdout: true)
        passthruString = passthruString.replaceAll('\n',' jenkins_')       
        env.BUILD_TIME = "${BUILD_TIMESTAMP}"
        def HUDSON_URL = "${env.HUDSON_URL}"
        echo "Workspace set to:" + env.WORKSPACE_LOCAL
        echo "Build time:" + env.BUILD_TIME
    }
    stage('Checkout Self') {
       echo "\n\n\n GIT CLONE STAGE"
        sh """
            rm -rf *
            ls -l
        """
        def branches = "${scm.branches}"
        if (branches.contains("master")) {
            git "${repoURL}"
        }
        if (branches.contains("main")) {
            git branch: "main", url: "${repoURL}"
        }
    }
    stage("BDD-Behave") {
        sh "wait 30"
    }"
}
    catch(e) {                           
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        throw e
    } finally {
        // Success or failure, always send notifications
        echo "I AM HERE"
        notifyBuild(currentBuild.result)
    }
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