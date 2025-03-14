import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

/**
 * Reusable component card for displaying different drone components
 *
 * @param {Object} props
 * @param {string} props.title - Card title displayed in the header
 * @param {object} props.icon - FontAwesome icon to display
 * @param {string} props.heading - Main heading for the card content
 * @param {string} props.description - Description text for the card
 * @param {string} props.colorType - Type of component for color styling (propulsion, control, frame, video, antenna)
 * @param {string} props.to - Link destination
 */
function ComponentCard({ title, icon, heading, description, colorType, to = "#" }) {
  // Map component types to their corresponding Tailwind border colors
  const colorMap = {
    propulsion: "border-propulsion-color",
    control: "border-control-color",
    frame: "border-frame-color",
    video: "border-video-color",
    antenna: "border-antenna-color",
  };

  // Map component types to their corresponding background colors for icons
  const bgColorMap = {
    propulsion: "bg-propulsion-color",
    control: "bg-control-color",
    frame: "bg-frame-color",
    video: "bg-video-color",
    antenna: "bg-antenna-color",
  };

  // Map component types to their corresponding text colors for headers
  const textColorMap = {
    propulsion: "text-propulsion-color",
    control: "text-control-color",
    frame: "text-frame-color",
    video: "text-video-color",
    antenna: "text-antenna-color",
  };

  const borderColor = colorMap[colorType] || colorMap.propulsion;
  const bgColor = bgColorMap[colorType] || bgColorMap.propulsion;
  const textColor = textColorMap[colorType] || textColorMap.propulsion;

  return (
    <Link
      to={to}
      className={`h-full bg-white rounded-lg overflow-hidden shadow-md transition-all duration-300 
                  flex flex-col no-underline text-text-color hover:translate-y-[-5px] hover:shadow-lg
                  border-t-4 ${borderColor}`}
    >
      <div className={`py-4 px-6 font-medium border-b border-gray-100 ${textColor}`}>
        {title}
      </div>
      <div className="p-6 flex items-start">
        <div className={`w-16 h-16 rounded-full flex justify-center items-center mr-5 flex-shrink-0 ${bgColor}`}>
          <i className="text-xl text-white">
            <FontAwesomeIcon icon={icon} />
          </i>
        </div>
        <div>
          <h4 className="text-lg font-medium mb-2 text-gray-800">{heading}</h4>
          <p className="text-sm text-gray-600 leading-relaxed">{description}</p>
        </div>
      </div>
    </Link>
  );
}

export default ComponentCard;