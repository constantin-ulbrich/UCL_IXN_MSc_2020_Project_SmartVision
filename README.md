# UCL_IXN_MSc_2020_Project_SmartVision

## What is this repository about?

This project aimed to propose and validate a new smart space service, using passive observer technology, for the Modern Workplace Practice of the technology consultancy Avanade. Specifically, the client was interested in learning about potential uses of the Azure Kinect DK sensor. The industry project was divided into a research and proof of concept component.

The research component anchors around the evaluation of potential use cases of the Microsoft Azure Kinect DK and its performance against competitive sensors. Also, insights about the Smart Space/IoT industry and its key players will be collected. The industry analysis revealed that the Smart Space/IoT industry is rapidly growing with strong competitive rivalry among its players. The dominant goal of the sample companies is to develop a plug-and-play IoT platform. A key trend of the players is to advance their analytics solutions to process optimisation systems. The findings of the competitive product mapping showed that the Azure Kinect DK is a highly competitive depth sensor, positioned as a quality leader, scoring the second highest in terms of functionality. Furthermore, the findings highlighted that the Kinect excels in use cases requiring several sensor functionalities. The core research goal regarding the identification of potential use cases for the Kinect DK was answered with five recommendations. These have been developed in the following areas of application: office space, industrial manufacturing and construction sites, retail, and medicine.

Out of the recommended use cases, it was decided to build a proof of concept application for the core functionalities of the office space use case, namely the SmartVision system. It aims to demonstrate new solutions for office space occupation measurement in an unassigned desk environment and sensing employee health through emotion detection. Avanade’s developers were interested that the SmartVision system would employ Azure Cognitive services technologies in connection with the Azure Kinect DK to evaluate their suitability and feasibility for smart space services. The system receives image captures of a workstation from the Kinect DK. This data is then analysed by the SmartVision algorithm. The algorithm uses a scoring system to determine whether a workstation is occupied by analysing the objects present on a desk. It detects the emotions of employees by analysing their facial expressions. The SmartVision algorithm utilizes the Azure Computer Vision and Face service and is complemented by a custom machine learning object detection model. The results of the analysis are stored in a MySQL database and an Azure Blob Storage. The developer team can view statistics of the analysis, as well as control and configure the SmartVision algorithm via a Flask web-application (e.g. adjusting the algorithm’s detection sensitivity). Moreover, the SmartVision system’s modular design enables the client to separately test the technology components and potentially expand the system into a full prototype of the envisioned use case.

## What does this repository contain?

This repository contains the research and proof of concept deliverable for the Smart Vision Industry Project with Avanade Inc.:
- SmartVision_ProofOfConcept_DeploymentandUserManuel_Constantin_Ulbrich_vFinalAvanade.pdf
- SmartVision_ResearchDeliverable_Constantin_Ulbrich_vFinalAvanade.pdf
- COMP0073_SmartVision_Project (Folder)
  - Azure_Kinect_Controller (Folder containing the Code to control the Azure Kinect DK Sensor)
  - COMP0073_SmartVision_Prototype (Folder containing all components of the SmartVision System)

The Master Thesis associated to this project can be requested from Avanade Inc., UCL, and the author (Constantin Ulbrich).

## Special Notes:

- Due to file size limitations on GitHub, the suitable Python Environment, which contained all the necessary libraries, could not be included. Instead a requirements.txt file has been added, which can be executed with the Pip installer to conveniently create your own environment.

- Also due to file size limitations, only the source code and the log files of the Azure Kinect Controller System could be uploaded. For a working prototype, a C++ Visual Studio project has to be created with the name "Azure_Kinect_Controller". Add the source code in a file with precisely the same name as uploaded. Make sure to include the libraries Azure Blob Storage and Azure Kinect Sensor SDK.

- Note, you require the following Azure Cognitive Services to run the proof of concept application: Azure Computer Vision, Azure Face, Azure Custom Vision, Azure Blob Storage. Configure these services in the config.py file in the folder SmartVision_DetectionAlgorithm.

- This project used a custom made detection model to detect objects, which are usually found on a workstation, to support the precision of the detection capabilities of the SmartVision system. Access to this model might be granted if permission is obtained from the author and Avanade.

- In case you are setting up a new blob storage account, the blob storage needs to consist of four containers with the names: "analysedframes", "frames", "lasttakenframe", and "tests".

# Other information

## Who is Avanade?

[Avanade](www.avanade.com) is the leading provider of innovative digital and cloud services, business solutions and design-led experiences on the Microsoft ecosystem, and the power behind the Accenture Microsoft Business Group.

## Emerging Technology

[Avanade Emerging Technologies](https://www.avanade.com/en-gb/thinking/research-and-insights/trendlines) helps clients not only see the future, but create it. Through applied research, experimentation, and collaboration, we empower them to make smart bets and achieve step changes in competitive advantage.
