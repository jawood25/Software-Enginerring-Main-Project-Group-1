# SwEng Main Project Group 1 performanceMeasurer
 Repository for Software Engineering Main Project Group 1 2022
 
 //INFO FOR TEAM MEMBERS TO START//
 
- TO WORK ON THIS WEB APP YOU NEED TO MAKE SURE YOU HAVE AN IDE THAT SUPPORTS JAVA JDK 17 OR IT WILL NOT WORK!!! I recommend using Intellij 2022 version.

To begin working in your IDE:
- Clone this repository
- Follow the tutorial at this link (use Java 17): https://docs.oracle.com/cd/E19182-01/821-0917/inst_jdk_javahome_t/index.html#:~:text=To%20set%20JAVA_HOME%2C%20do%20the,Program%20Files%5CJava%5Cjdk1
- Restart your PC before continuing

To check that things are set up correctly (and this is how to open the web app):
- Open up the repository in your IDE
- Open up the IDE terminal
- In your teminal type: ./mvnw spring-boot:run
- Now in your browser go to: http://localhost:8080/performanceMeasurer
- You should just see a web page for now which just says "Hello World!", this is just the basic setup for the web app so obviously there isn't any proper code yet.

-- TO TEAMMATES WHO ARE WORKING ON THE CODE --

- The file src/main/java/com/group1/performancemeasurer/PerformanceMeasurerController.java is like the main backend code. Feel free to create other java classes in the same folder that are used in this class, but those files should not have a "main" otherwise the web app will not work.

- To work on the unit tests for the application, please type in the file: src/test/java/com/group1/performancemeasurer/PerformanceMeasurerApplicationTests.java

- If you want to work on the GUI in HTML, the file to work on that is: src/main/resources/templates/performanceMeasurerGUI.html

I will try to set up a CI workflow as soon as possible so that if anybody writes any unit tests they will be checked whenever somebody makes a pull request.

-Jason
