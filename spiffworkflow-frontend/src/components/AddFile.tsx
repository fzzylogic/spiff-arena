import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import { Dropdown, FileUploader, Modal } from '@carbon/react';
import HttpService from '../services/HttpService';
import useAPIError from '../hooks/UseApiError';

import { modifyProcessIdentifierForPathParam } from '../helpers';
import { ProcessModel } from '../interfaces';

export default function AddFile() {
  const params = useParams();
  const { addError, removeError } = useAPIError();
  const navigate = useNavigate();

  const [processModel, setProcessModel] = useState<ProcessModel | null>(null);
  const [reloadModel, setReloadModel] = useState<boolean>(false);
  const [filesToUpload, setFilesToUpload] = useState<any>(null);
  const [showFileUploadModal, setShowFileUploadModal] =
    useState<boolean>(false);

  const modifiedProcessModelId = modifyProcessIdentifierForPathParam(
    `${params.process_model_id}`
  );

  const onUploadedCallback = () => {
    setReloadModel(true);
  };

  const [fileUploadEvent, setFileUploadEvent] = useState(null);
  const [duplicateFilename, setDuplicateFilename] = useState<String>('');
  const [showOverwriteConfirmationPrompt, setShowOverwriteConfirmationPrompt] =
    useState(false);

  const doFileUpload = (event: any) => {
    event.preventDefault();
    removeError();
    const url = `/process-models/${modifiedProcessModelId}/files`;
    const formData = new FormData();
    formData.append('file', filesToUpload[0]);
    formData.append('fileName', filesToUpload[0].name);
    HttpService.makeCallToBackend({
      path: url,
      successCallback: onUploadedCallback,
      httpMethod: 'POST',
      postBody: formData,
      failureCallback: addError,
    });
    setFilesToUpload(null);
  };

  const handleFileUploadCancel = () => {
    setShowFileUploadModal(false);
    setFilesToUpload(null);
  };
  const handleOverwriteFileConfirm = () => {
    setShowOverwriteConfirmationPrompt(false);
    doFileUpload(fileUploadEvent);
  };
  const handleOverwriteFileCancel = () => {
    setShowOverwriteConfirmationPrompt(false);
    setFilesToUpload(null);
  };

  const confirmOverwriteFileDialog = () => {
    return (
      <Modal
        danger
        open={showOverwriteConfirmationPrompt}
        data-qa="file-overwrite-modal-confirmation-dialog"
        modalHeading={`Overwrite the file: ${duplicateFilename}`}
        modalLabel="Overwrite file?"
        primaryButtonText="Yes"
        secondaryButtonText="Cancel"
        onSecondarySubmit={handleOverwriteFileCancel}
        onRequestSubmit={handleOverwriteFileConfirm}
        onRequestClose={handleOverwriteFileCancel}
      />
    );
  };
  const displayOverwriteConfirmation = (filename: String) => {
    setDuplicateFilename(filename);
    setShowOverwriteConfirmationPrompt(true);
  };

  const checkDuplicateFile = (event: any) => {
    if (processModel) {
      let foundExistingFile = false;
      if (processModel.files.length > 0) {
        processModel.files.forEach((file) => {
          if (file.name === filesToUpload[0].name) {
            foundExistingFile = true;
          }
        });
      }
      if (foundExistingFile) {
        displayOverwriteConfirmation(filesToUpload[0].name);
        setFileUploadEvent(event);
      } else {
        doFileUpload(event);
      }
    }
    return null;
  };

  const handleFileUpload = (event: any) => {
    checkDuplicateFile(event);
    setShowFileUploadModal(false);
  };

  const fileUploadModal = () => {
    return (
      <Modal
        data-qa="modal-upload-file-dialog"
        open={showFileUploadModal}
        modalHeading="Upload File"
        primaryButtonText="Upload"
        secondaryButtonText="Cancel"
        onSecondarySubmit={handleFileUploadCancel}
        onRequestClose={handleFileUploadCancel}
        onRequestSubmit={handleFileUpload}
      >
        <FileUploader
          labelTitle="Upload files"
          labelDescription="Max file size is 500mb. Only .bpmn, .dmn, .json, and .md files are supported."
          buttonLabel="Add file"
          buttonKind="primary"
          size="md"
          filenameStatus="edit"
          role="button"
          accept={['.bpmn', '.dmn', '.json', '.md']}
          disabled={false}
          iconDescription="Delete file"
          name=""
          multiple={false}
          onDelete={() => setFilesToUpload(null)}
          onChange={(event: any) => setFilesToUpload(event.target.files)}
        />
      </Modal>
    );
  };

  const items = [
    'Upload File',
    'New BPMN File',
    'New DMN File',
    'New JSON File',
    'New Markdown File',
  ].map((item) => ({
    text: item,
  }));

  return (
    <>
      {fileUploadModal()}
      {confirmOverwriteFileDialog()}
      <Dropdown
        id="inline"
        titleText=""
        size="lg"
        label="Add File"
        type="default"
        data-qa="process-model-add-file"
        onChange={(a: any) => {
          if (a.selectedItem.text === 'New BPMN File') {
            navigate(
              `/editor/process-models/${modifiedProcessModelId}/files?file_type=bpmn`
            );
          } else if (a.selectedItem.text === 'Upload File') {
            setShowFileUploadModal(true);
          } else if (a.selectedItem.text === 'New DMN File') {
            navigate(
              `/editor/process-models/${modifiedProcessModelId}/files?file_type=dmn`
            );
          } else if (a.selectedItem.text === 'New JSON File') {
            navigate(
              `/process-models/${modifiedProcessModelId}/form?file_ext=json`
            );
          } else if (a.selectedItem.text === 'New Markdown File') {
            navigate(
              `/process-models/${modifiedProcessModelId}/form?file_ext=md`
            );
          } else {
            console.log('a.selectedItem.text', a.selectedItem.text);
          }
        }}
        items={items}
        itemToString={(item: any) => (item ? item.text : '')}
      />
    </>
  );
}
