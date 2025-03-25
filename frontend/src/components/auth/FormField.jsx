import React from 'react';
import PropTypes from 'prop-types';

/**
 * Reusable form field component with icon and error handling
 */
const FormField = ({
  id,
  label,
  type = 'text',
  placeholder,
  icon,
  register,
  errors,
  required = false,
  ...rest
}) => {
  return (
    <div className="mb-6">
      <label htmlFor={id} className="block font-medium mb-2 text-primary">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <div className="relative">
        {icon && (
          <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
            {icon}
          </span>
        )}
        <input
          id={id}
          type={type}
          className={`w-full py-3 ${icon ? 'pl-10' : 'pl-4'} pr-4 border 
            ${errors?.[id] ? 'border-red-500' : 'border-gray-200'} rounded-lg text-base 
            transition-all focus:outline-none focus:border-secondary focus:ring-2 
            focus:ring-secondary focus:ring-opacity-20`}
          placeholder={placeholder}
          {...register(id, { required: required && `${label} is required` })}
          {...rest}
        />
      </div>
      {errors?.[id] && (
        <p className="text-red-500 text-sm mt-1">{errors[id].message}</p>
      )}
    </div>
  );
};

FormField.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  type: PropTypes.string,
  placeholder: PropTypes.string,
  icon: PropTypes.node,
  register: PropTypes.func.isRequired,
  errors: PropTypes.object,
  required: PropTypes.bool
};

export default FormField;