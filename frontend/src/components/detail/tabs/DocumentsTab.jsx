import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faFilePdf,
  faFileAlt,
  faFileImage,
  faFileArchive,
  faFileExcel,
  faFileWord,
  faFile,
  faEye,
  faDownload
} from '@fortawesome/free-solid-svg-icons';
import TabSection from '../TabSection';
import { themeClasses } from '../../../utils/themeUtils';

/**
 * Documents tab content for component detail page
 */
const DocumentsTab = ({ item, themeColor }) => {
  const themeClass = themeClasses[themeColor] || themeClasses.primary;

  const getDocumentIcon = (fileUrl) => {
    if (!fileUrl) return faFile;

    const extension = fileUrl.split('.').pop().toLowerCase();

    switch (extension) {
      case 'pdf':
        return faFilePdf;
      case 'txt':
      case 'rtf':
        return faFileAlt;
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif':
        return faFileImage;
      case 'zip':
      case 'rar':
      case '7z':
        return faFileArchive;
      case 'xls':
      case 'xlsx':
        return faFileExcel;
      case 'doc':
      case 'docx':
        return faFileWord;
      default:
        return faFile;
    }
  };

  const getDocumentType = (fileUrl) => {
    if (!fileUrl) return 'Unknown';

    const extension = fileUrl.split('.').pop().toLowerCase();

    switch (extension) {
      case 'pdf':
        return 'PDF';
      case 'txt':
        return 'Text';
      case 'rtf':
        return 'Rich Text';
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif':
        return 'Image';
      case 'zip':
      case 'rar':
      case '7z':
        return 'Archive';
      case 'xls':
      case 'xlsx':
        return 'Excel';
      case 'doc':
      case 'docx':
        return 'Word';
      default:
        return extension.toUpperCase();
    }
  };

  const getFileSize = (size) => {
    if (!size || isNaN(size)) return 'Unknown';

    if (size < 1024) {
      return `${size} B`;
    } else if (size < 1024 * 1024) {
      return `${(size / 1024).toFixed(1)} KB`;
    } else {
      return `${(size / (1024 * 1024)).toFixed(1)} MB`;
    }
  };

  // If no documents, show a message
  if (!item.documents || item.documents.length === 0) {
    return (
      <TabSection title="Documents" themeColor={themeColor}>
        <p className="text-gray-500 italic">No documents available for this component.</p>
      </TabSection>
    );
  }

  return (
    <TabSection title="Documents" themeColor={themeColor}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {item.documents.map((doc, index) => (
          <div
            key={index}
            className="bg-gray-50 rounded-xl p-4 flex items-center transition-all hover:bg-gray-100 hover:-translate-y-1"
          >
            <div className={`${themeClass.bg} text-white w-12 h-12 flex-shrink-0 rounded-lg flex items-center justify-center mr-4`}>
              <FontAwesomeIcon icon={getDocumentIcon(doc.file)} size="lg" />
            </div>

            <div className="flex-grow min-w-0">
              <h4 className="font-medium text-primary truncate">{doc.file.split('/').pop()}</h4>
              <div className="text-xs text-gray-500">
                {getDocumentType(doc.file)} • {getFileSize(doc.size)}
              </div>
            </div>

            <div className="flex-shrink-0 ml-4 flex gap-2">
              <a
                href={doc.file}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => {
                  e.preventDefault();
                  window.open(doc.file, '_blank', 'noopener,noreferrer');
                }}
                className={`w-8 h-8 flex items-center justify-center ${themeClass.border} ${themeClass.text} rounded hover:${themeClass.bg} hover:text-white transition-colors`}
                title="View document"
              >
                <FontAwesomeIcon icon={faEye} />
              </a>
              <a
                href={doc.file}
                download
                className={`w-8 h-8 flex items-center justify-center ${themeClass.border} ${themeClass.text} rounded hover:${themeClass.bg} hover:text-white transition-colors`}
                title="Download document"
              >
                <FontAwesomeIcon icon={faDownload} />
              </a>
            </div>
          </div>
        ))}
      </div>
    </TabSection>
  );
};

DocumentsTab.propTypes = {
  item: PropTypes.object.isRequired,
  themeColor: PropTypes.string.isRequired
};

export default DocumentsTab;