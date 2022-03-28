# dtc_de_nifi_project
DTC DE Zoom Camp Project : Nifi ETL Processor

In this project we will be using Apache NiFi to download the data from the NOAA site.

Later in the process, we will be using the Google Map API to lookup the location corresponding to the latitude and longitude of the NOAA weather stations. In prepration, request a Map API key from <a href="https://console.cloud.google.com/project/_/google/maps-apis/credentials">APIs &amp; Services→Credentials</a>. As suggested in the documentation, secure the key by limiting access to the key from the IP of your server.
Save the value to the GCP_API_KEY in your .bashrc as below. Note that <USER> will be need to be replace with the correct user id on the server.


SSH into the ETL server using the following:
<pre>
export ETL_SERVER=my-etl-server;
gcloud compute ssh ${ETL_SERVER=} --zone=us-central1-c
</pre>
  
  
The NiFi appliation will be secured with the user ID and password stored in the environment variables  SINGLE_USER_CREDENTIALS_USERNAME and SINGLE_USER_CREDENTIALS_PASSWORD, respectively.
  
Edit the <a href="https://github.com/ptking777/dtc_de_nifi_project/blob/main/docker-compose.yml">docker-compose.yml</a> file and change <USER> to the correct user ID.  
  
Also, please ensure the GOOGLE_APPLICATION_CREDENTIALS in ./bashrc points to your Google Credentials file.  
Note that the GOOGLE_APPLICATION_CREDENTIALS  file needs to be readablt from the NiFi container.
Run the following: 
<pre>
sudo chown 1000:1000 $GOOGLE_APPLICATION_CREDENTIALS
sudo chmod ug+r $GOOGLE_APPLICATION_CREDENTIALS
ls -l credentials/google_credentials.json
-r--r----- 1 ubuntu ubuntu 2329 Mar 28 02:16 credentials/google_credentials.json
</pre>


Edit the ~/.bashrc to include the following:
<pre>
export GOOGLE_APPLICATION_CREDENTIALS=/home/<USER>/.ssh/.google/credentials/google_credentials.json
export SINGLE_USER_CREDENTIALS_USERNAME=admin
export SINGLE_USER_CREDENTIALS_PASSWORD=<?????>
export GCP_API_KEY=<?????>
</pre>

Launch NiFI in Docker using docker compose.
If you have not already done so, clone the repository:
<pre>
git clone git@github.com:ptking777/dtc_de_nifi_project.git
cd dtc_de_nifi_project
</pre>
<p>
Launch Apache Nifi by executint: <i>docker-compose up -d</i>. The NiFi application should now be runnning on port 8443.
We will need to setup port forwarding to facilitate access. In another terminal, execute the following.
<pre>
gcloud compute  ssh --ssh-flag="-L 8443:localhost:8443"  --zone "us-central1-c" my-etl-server
</pre>
You should now be able to access the NiFi using your browser at the following address: <i>https://localhost:8443/nifi<i>.
You will need to enter the userID/password you created above.
<p>
Note: The NiFi controller services will need to be enabled before running the transformation.

For a quick introduction to Apachi Nifi, please see the tutorial <a href="https://youtu.be/VVnFt54jUQ8">Apache NiFi Tutorial - Complete Guide (Part 1) - Course Introduction</a> on YouTube.




