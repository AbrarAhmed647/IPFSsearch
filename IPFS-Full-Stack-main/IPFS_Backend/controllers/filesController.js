const ipfs = require("ipfs-http-client");
const fs = require('fs');
const { spawn } = require('child_process');
const path = require('path');
const WebSocket = require("ws");

const ipfsClient = ipfs.create('/ip4/127.0.0.1/tcp/5001');                  // TO-DO: We need to make it so the user doesn't need to manually change the path to the json 
                                                                              // (both python scripts need it) and the server's ip and port (index_sender.py needs it)
                                                                              // this is currently hard coded

const getAllFilesByNameAndCID = async (req, res) => {
    const localFiles = await ipfsClient.files.ls('/');
    const files = [];

    for await (const file of localFiles) {
        if (!file.type || file.type === "file") {
            files.push({ cid: file.cid.toString(), name: file.name });
        }
      }

      res.json(files);


}

const sendSelectedFilesContent = async (req, res) => {
    const selectedFiles = req.body;
    const cidList = [];
    const cidContents = [];

    for await (const file of selectedFiles) {
        if (!file.type || file.type === "file") {
            cidList.push(file.cid.toString());
        }
      }
        console.log(cidList);

        for await (const cid of cidList) {
            const result = await ipfsClient.cat(cid);
            let contents = "";
            for await (const item of result) {
                contents += new TextDecoder().decode(item);
            }
            contents = contents.replace(/\0/g, "");
            // const input = {cid, contents};
            // let data = JSON.stringify(input);
            // fs.writeFileSync('cid_content.json', data);           
            
            cidContents.push({ cid, contents});
        }
        console.log(cidContents);
      
        sendInvertedJsonContent(cidContents);
}

async function sendInvertedJsonContent(cidContents) {
  const invertedJsonContent = await runPythonScript(cidContents);
  console.log(invertedJsonContent);

  // Joaquin: Changed this to call the "index_sender.py" script instead of connecting with the server directly
  jsonFilePath = path.join(__dirname, '..', 'controllers', 'index', 'inverted_index.json');
  sendJsonFile(jsonFilePath)
    .then(() => {
      console.log("JSON file sent successfully.");
    })
    .catch((error) => {
      console.error("Python script failed", error);
    });
  
 
}

// Joaquin: I edited this so that when called, the program won't continue until this finishes executing 
const runPythonScript = async (data) => {
  const pythonScriptPath = path.join(__dirname, '..', 'controllers', 'index_builder_txt.py');
  const pythonProcess = spawn('python', [pythonScriptPath, JSON.stringify(data)]);

  const promise = new Promise((resolve, reject) => {
    let output = '';
    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python script stderr: ${data}`);
      reject(data);
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
        reject(code);
      } else {
        console.log(`Python script stdout: ${output}`);
        resolve();
      }
    });
  });

  await promise;

  const invertedFilrPath = path.join(__dirname, '..', 'controllers','index', 'inverted_index.json');
  
  const fileContent = fs.readFileSync(invertedFilrPath, "utf8");

  return fileContent;
};

// Joaquin: Added this function to call the new python script in charge of sending the JSON file
const sendJsonFile = async (jsonFilePath) => {
  const pythonScriptPath = path.join(__dirname, '..', 'controllers', 'index_sender.py');
  const pythonProcess = spawn('python', [pythonScriptPath, '-json_path', jsonFilePath]);

  const promise = new Promise((resolve, reject) => {
    let output = '';
    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python script stderr: ${data}`);
      reject(data);
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
        reject(code);
      } else {
        console.log(`Python script stdout: ${output}`);
        resolve();
      }
    });
  });

  await promise;
};


module.exports = { sendSelectedFilesContent, getAllFilesByNameAndCID }