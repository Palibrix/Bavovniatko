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
  // Get the appropriate color classes based on component type
  const getColorClasses = (type) => {
    const types = {
      propulsion: {
        border: "border-propulsion",
        text: "text-propulsion",
        bg: "bg-propulsion"
      },
      control: {
        border: "border-control",
        text: "text-control",
        bg: "bg-control"
      },
      frame: {
        border: "border-frame",
        text: "text-frame",
        bg: "bg-frame"
      },
      video: {
        border: "border-video",
        text: "text-video",
        bg: "bg-video"
      },
      antenna: {
        border: "border-antenna",
        text: "text-antenna",
        bg: "bg-antenna"
      }
    };

    // Return the default (propulsion) if the provided type isn't valid
    return types[type] || types.propulsion;
  };

  const colors = getColorClasses(colorType);

  return (
    <Link
      to={to}
      className={`h-full bg-white rounded-lg overflow-hidden shadow-md transition-all duration-300 
                  flex flex-col no-underline text-text-color hover:translate-y-[-5px] hover:shadow-lg
                  border-t-4 ${colors.border}`}
    >
      <div className={`py-4 px-6 font-medium border-b border-gray-100 ${colors.text}`}>
        {title}
      </div>
      <div className="p-6 flex items-start">
        <div className={`w-16 h-16 rounded-full flex justify-center items-center mr-5 flex-shrink-0 ${colors.bg} text-white`}>
          <i className="text-xl">
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