import React, {useState} from 'react';
import "./Upload.css"
export default function Upload() {
    const[files, setFiles] = useState([])
    const[uploadText,setUploadText] = useState('Files not uploaded')
    function handleMultipleChange(event) {

        setFiles([...event.target.files]);
    }

    function handleMultipleSubmits(e){
        e.preventDefault();
        if(files.length){
            const formData = new FormData();
            files.forEach((file, index) => {
              formData.append(`file${index}`, file);
            });
            setUploadText('Files Uploaded!')
        }
        else{
            setUploadText('No Files included! Please upload files!')

        }
    }
    return (
    <div className="upload">
        <form onSubmit={handleMultipleSubmits}>
            <h1>Upload File</h1>
            <h3 className='ifUplodaed'>{uploadText}</h3>
            <div>
                <input type = "file" multiple onChange={handleMultipleChange}/>
                <button>Upload</button>
            </div>
        </form>       

         
    </div>
    )
}