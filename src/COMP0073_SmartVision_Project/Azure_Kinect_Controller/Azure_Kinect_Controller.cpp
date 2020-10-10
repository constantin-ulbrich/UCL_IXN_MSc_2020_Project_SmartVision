// Module Description: This module steers the Azure Kinect DK, takes a Depth, IR, and Color image and uploads the color image to the blob storage of the SmartVision System
// Also note, that certain parts of the code (SaveImage, and aspects of capturing the images) were created in collaboration with the Avanade Specialist.
#pragma comment(lib, "k4a.lib")
#include <k4a/k4a.h>
#include <k4arecord/record.h>
#include <stdio.h>
#include <stdlib.h>
#include <fstream> 
#include <was/storage_account.h>
#include <was/blob.h>
#include <cpprest/filestream.h>  
#include <cpprest/containerstream.h> 


// The function was developed from the original idea of the following code snippet: https://stackoverflow.com/questions/57331989/azure-kinect-recording-color-format
long SaveImage(const char* imageName, void* buffer, size_t bufferSize)
{
    // Write the image to a buffer for further processing

    std::ofstream outfile(imageName, std::ofstream::binary);

    // write to outfile
    outfile.write((char*)buffer, bufferSize);

    outfile.close();

    printf("Successfully writen the image: %s\n", imageName);

    return 0;
}


void uploadImageToBlob() {
    // The following code for the blob storage access and upload of an image has been adapted from 
        //the Microsoft Documentation: https://docs.microsoft.com/en-us/azure/storage/blobs/storage-c-plus-plus-how-to-use-blobs
        // Define the connection-string with your values.
    const utility::string_t blob_storage_connection_string(U("[Insert your Azure Blob Storage Connection String]"));

    // Connecting to the Azure Blob Storage Account of the SmartVision System
    azure::storage::cloud_storage_account blob_storage_account = azure::storage::cloud_storage_account::parse(blob_storage_connection_string);

    // Request a blob client to manipulate the blob storage
    azure::storage::cloud_blob_client blob_storage_client = blob_storage_account.create_cloud_blob_client();

    // Obtain access to container "frames" in the SmartVision Blob Storage
    azure::storage::cloud_blob_container container_frames = blob_storage_client.get_container_reference(U("frames"));

    // Attempt to access the blob "tester.jpg". If it does not exist, it will create a new blob instance with this name.
    azure::storage::cloud_block_blob blockBlob_image1 = container_frames.get_block_blob_reference(U("tester.jpg"));

    // Write file into the just created "tester.jpg" blob, or overwrite existing "tester.jpg" blob.
    concurrency::streams::istream input_stream1 = concurrency::streams::file_stream<uint8_t>::open_istream(U("colorImage.jpg")).get();
    blockBlob_image1.upload_from_stream(input_stream1);
    input_stream1.close().wait();

    // Obtain access to container "lasttakenframe" in the SmartVision Blob Storage
    azure::storage::cloud_blob_container container_lastTakenFrame = blob_storage_client.get_container_reference(U("lasttakenframe"));

    // Attempt to access the blob "tester.jpg". If it does not exist, it will create a new blob instance with this name.
    azure::storage::cloud_block_blob blockBlob_image2 = container_lastTakenFrame.get_block_blob_reference(U("tester.jpg"));

    // Write file into the just created "tester.jpg" blob, or overwrite existing "tester.jpg" blob.
    concurrency::streams::istream input_stream2 = concurrency::streams::file_stream<uint8_t>::open_istream(U("colorImage.jpg")).get();
    blockBlob_image2.upload_from_stream(input_stream2);
    input_stream2.close().wait();

    /*
    // For System Tests, the image is uploaded to the "tests" container in the SmartVision Azure Blob Storage System
    // Obtain access to container "tests" in the SmartVision Blob Storage
    azure::storage::cloud_blob_container container = blob_storage_client.get_container_reference(U("tests"));

    // Attempt to access the blob "tester.jpg". If it does not exist, it will create a new blob instance with this name.
    azure::storage::cloud_block_blob blockBlob = container.get_block_blob_reference(U("testImageCPP.jpg"));

    // Write file into the just created "tester.jpg" blob, or overwrite existing "tester.jpg" blob.
    concurrency::streams::istream input_stream = concurrency::streams::file_stream<uint8_t>::open_istream(U("colorImage.jpg")).get();
    blockBlob.upload_from_stream(input_stream);
    input_stream.close().wait();
    */
}


int main() {
    // The following code was adopted from the provided documentation and documentation examples found at the source: https://docs.microsoft.com/en-us/azure/kinect-dk/retrieve-images
    // Note, logging as been prompted and initializing on the machine of the developer of the SmartVision System

    int TIMEOUT_IN_MS = 5000;
	printf("We are in the azure_kinect_controller script.\n"); // Control statement for testing purposes
    
    k4a_device_t device = NULL;
    k4a_capture_t capture = NULL;

    k4a_device_configuration_t config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
    config.camera_fps = K4A_FRAMES_PER_SECOND_15;
    config.color_format = K4A_IMAGE_FORMAT_COLOR_MJPG;
    config.synchronized_images_only = true;
    // Usual Color image resolution and depth mode resolution:
    config.color_resolution = K4A_COLOR_RESOLUTION_2160P;
    config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
    //Configuration when attempting to transfor the depth image into the color image format:
    //config.color_resolution = K4A_COLOR_RESOLUTION_720P;
    //config.depth_mode = K4A_DEPTH_MODE_WFOV_UNBINNED;


    // Open the Kinect DK
    if (K4A_FAILED(k4a_device_open(K4A_DEVICE_DEFAULT, &device)))
    {
        printf("Failed to open k4a device!\n");
        return 0;
    }
    else {
        printf("Kinect is switched on!\n");
    }

    // Starting up the Kinect DK
    if (K4A_RESULT_SUCCEEDED != k4a_device_start_cameras(device, &config))
    {
        printf("Failed to start device\n");
        exit(0);
    }
    else {
        printf("Camera Started\n");
    }


    // Capturing visual data with the visual sensors of the Kinect DK
    switch (k4a_device_get_capture(device, &capture, TIMEOUT_IN_MS))
    {
    case K4A_WAIT_RESULT_SUCCEEDED:
        printf("Capture Success\n");
        break;
    case K4A_WAIT_RESULT_TIMEOUT:
        printf("Timed out waiting for a capture\n");
        exit(0);
    case K4A_WAIT_RESULT_FAILED:
        printf("Failed to read a capture\n");
        exit(0);
    }


    // Retrieving the image of the color image
    k4a_image_t image = k4a_capture_get_color_image(capture);
    
    // Check that a color image has been captured
    if (image)
    {
        //Writing the Color image to the output folder using the SaveImage function
        SaveImage("colorImage.jpg", k4a_image_get_buffer(image), k4a_image_get_size(image));
        
        printf("Color Image Capture --> Resoluation: %4d x %4d | Stride:%5d\n",
            k4a_image_get_height_pixels(image),
            k4a_image_get_width_pixels(image),
            k4a_image_get_stride_bytes(image));

        // Release the image
        k4a_image_release(image);
    }
    else {
        printf("Image is null!\n");
    }
  
    /*
    // Capturing an IR image
    k4a_image_t ir_image = k4a_capture_get_ir_image(capture);

    // Check that the IR image has been cpatured successfully
    if (ir_image)
    {
        printf("IR Image Capture --> Resoluation: %4d x %4d | Stride:%5d\n",
            k4a_image_get_height_pixels(ir_image),
            k4a_image_get_width_pixels(ir_image),
            k4a_image_get_stride_bytes(ir_image));

        // Release the image
        k4a_image_release(ir_image);
    }
    else {
        printf("Image is null!\n");
    }
    */

    // Retrieving the capture of the depth image
    k4a_image_t depth_image = k4a_capture_get_depth_image(capture);

    if (depth_image)
    {
        //SaveImage("depthImage.bin", k4a_image_get_buffer(depth_image), k4a_image_get_size(depth_image));

        printf("Depth Image Capture --> Resoluation: %4d x %4d | Stride:%5d\n",
            k4a_image_get_height_pixels(depth_image),
            k4a_image_get_width_pixels(depth_image),
            k4a_image_get_stride_bytes(depth_image));

        
        // Transforming the depth image with the color image to an RGB-D image of the format of the Color image
        // Coding concepts were adapted from the source: https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/examples/transformation/main.cpp
        k4a_image_t transformed_depth_image = NULL;
        int color_image_height_pixels = k4a_image_get_height_pixels(image);
        int color_image_width_pixels = k4a_image_get_width_pixels(image);

        // Setting up the necessary calibration of the device for the transformation
        k4a_calibration_t calibration;
        if (K4A_RESULT_SUCCEEDED !=
            k4a_device_get_calibration(device, config.depth_mode, config.color_resolution, &calibration))
        {
            printf("Failed to get calibration\n");
            return 0;
        }

        // Preparing the image, in which the transformed image will be saved
        if (K4A_RESULT_SUCCEEDED != k4a_image_create(K4A_IMAGE_FORMAT_DEPTH16,
            color_image_width_pixels,
            color_image_height_pixels,
            color_image_width_pixels * (int)sizeof(uint16_t),
            &transformed_depth_image))
        {
            printf("Failed to create transformed depth image\n");
            return false;
        }

        // Preparing the transformation
        k4a_transformation_t transformation = k4a_transformation_create(&calibration);
        // Executing the transformation
        if (K4A_RESULT_SUCCEEDED !=
            k4a_transformation_depth_image_to_color_camera(transformation, depth_image, transformed_depth_image))
        {
            printf("Failed to compute transformed depth image\n");
            return false;
        }

        // Checking key characteristics of the transfored depth image
        printf("Transformed Depth Image --> Resoluation: %4d x %4d | Stride:%5d\n",
            k4a_image_get_height_pixels(transformed_depth_image),
            k4a_image_get_width_pixels(transformed_depth_image),
            k4a_image_get_stride_bytes(transformed_depth_image));

  
        /*
        // Attempt to write a recording in order to save the transformed depth image or the original depth image.
        // However, this attempt failed to save the images in the correct format (Source: https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/examples/k4arecord_custom_track/main.c)
        k4a_record_t recording;

        if (K4A_FAILED(k4a_record_create("TestFile.mvk", device, config, &recording)))
        {
            printf("Unable to create recording file: TestFile\n");
            return 1;
        }

        k4a_record_write_header(recording);

        uint8_t* depth_buffer = k4a_image_get_buffer(transformed_depth_image);
        size_t depth_buffer_size = k4a_image_get_size(transformed_depth_image);

        k4a_record_write_custom_track_data(recording, "TRANSFORMED_DEPTH.png", k4a_image_get_device_timestamp_usec(transformed_depth_image), depth_buffer,
            (uint16_t)depth_buffer_size);

        printf("Saving recording...\n");
        k4a_record_flush(recording);
        k4a_record_close(recording);

        */

        //Writing the Color image to the output folder using the SaveImage function
        SaveImage("transformedDepthImage.bin", k4a_image_get_buffer(transformed_depth_image), k4a_image_get_size(transformed_depth_image));

        k4a_image_release(transformed_depth_image);

        /*
        // Testing to obtain the depth data of the depth image...
        int width = k4a_image_get_width_pixels(depth_image);
        int height = k4a_image_get_height_pixels(depth_image);
        uint16_t *depth_data = (uint16_t*)(void*)k4a_image_get_buffer(depth_image);
        printf("Depth Array:\n");
        printf("%d ", (int)depth_data);
        for (int i = 0; i < width * height; i++)
        {
            printf("Depth datapoint: %d\n", depth_data[i]);
        }
        */

        // Release the image
        k4a_image_release(depth_image);
    }
    else {
        printf("Image is null!\n");
    }


    // Release the capture
    k4a_capture_release(capture);

    if (device != NULL)
    {
        k4a_device_stop_cameras(device);
        k4a_device_close(device);
    }

    // Uploading the captured image to the blob storage of the SmartVision System
    uploadImageToBlob();

    return 0;
}