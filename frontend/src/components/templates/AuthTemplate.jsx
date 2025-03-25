import React, {useState} from 'react';
import {useForm} from 'react-hook-form';
import {useNavigate} from 'react-router-dom';
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faEye, faEyeSlash, faUser, faEnvelope, faLock} from '@fortawesome/free-solid-svg-icons';
import {useAuth} from '../../context/AuthContext';
import FormField from '../auth/FormField';
import PasswordStrengthMeter from '../auth/PasswordStrengthMeter';

/**
 * Authentication template component with tabs for login and registration
 */
const AuthTemplate = ({initialTab = 'login'}) => {
    const [activeTab, setActiveTab] = useState(initialTab);
    const [notification, setNotification] = useState({message: '', type: ''});
    const [showLoginPassword, setShowLoginPassword] = useState(false);
    const [showRegisterPassword, setShowRegisterPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const {login, register: registerUser} = useAuth();
    const navigate = useNavigate();

    // React Hook Form for login
    const {
        register: registerLoginField,
        handleSubmit: handleLoginSubmit,
        formState: {errors: loginErrors, isSubmitting: isLoginSubmitting}
    } = useForm();

    // React Hook Form for registration
    const {
        register: registerRegisterField,
        handleSubmit: handleRegisterSubmit,
        formState: {errors: registerErrors, isSubmitting: isRegisterSubmitting},
        watch,
        getValues
    } = useForm();

    // Watch password field for password strength meter
    const watchPassword = watch('password', '');

    // Handle tab switching
    const switchTab = (tab) => {
        setActiveTab(tab);
    };

    // Handle login form submission
    const onLogin = async (data) => {
        try {
            await login(data);
            setNotification({
                message: 'Successfully logged in!',
                type: 'success'
            });
            navigate('/');
        } catch (error) {
            setNotification({
                message: error.data || 'Failed to login. Please try again.',
                type: 'error'
            });
        }
    };

    // Handle registration form submission
    const onRegister = async (data) => {
        if (data.password !== data.confirmPassword) {
            setNotification({
                message: 'Passwords do not match',
                type: 'error'
            });
            return;
        }

        try {
            const userData = {
                username: data.username,
                email: data.email,
                password: data.password,
                profile: {
                    first_name: data.firstName,
                    last_name: data.lastName || ''
                }
            };

            await registerUser(userData);
            setNotification({
                message: 'Registration successful! Please log in.',
                type: 'success'
            });

            switchTab('login');
        } catch (error) {

            setNotification({
                message: error.data || 'Registration failed. Please try again.',
                type: 'error'
            });
        }
    };

    return (
        <div className="w-[90%] max-w-[500px] mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-primary text-center mb-8 relative">
                Account Access
                <span className="block w-14 h-1 bg-secondary mx-auto mt-2"></span>
            </h1>

            {/* Notification */}
            {notification.message && (
                <div className={`mb-6 p-4 rounded-lg text-white relative ${
                    notification.type === 'success' ? 'bg-green-500' : 'bg-red-500'
                }`}>
                    {typeof notification.message === 'string' ? (
                        notification.message
                    ) : (
                        <ul className="list-disc pl-5">
                            {Object.entries(notification.message).map(([key, error]) => (
                                <li key={key} className="mb-1">
                                    <strong>{key}:</strong> {error}
                                </li>
                            ))}
                        </ul>
                    )}
                    <button
                        onClick={() => setNotification({message: '', type: ''})}
                        className="absolute top-2 right-2 text-white"
                    >
                        &times;
                    </button>
                </div>
            )}

            <div className="bg-white rounded-3xl overflow-hidden shadow-md border-t-4 border-t-secondary">
                {/* Tab navigation */}
                <div className="flex border-b border-gray-100">
                    <div
                        className={`flex-1 text-center py-4 font-semibold cursor-pointer transition-all relative
              ${activeTab === 'login' ? 'text-secondary' : 'hover:bg-secondary hover:bg-opacity-5'}`}
                        onClick={() => switchTab('login')}
                    >
                        Login
                        {activeTab === 'login' && (
                            <span className="absolute bottom-0 left-[20%] w-[60%] h-[3px] bg-secondary"></span>
                        )}
                    </div>
                    <div
                        className={`flex-1 text-center py-4 font-semibold cursor-pointer transition-all relative
              ${activeTab === 'register' ? 'text-secondary' : 'hover:bg-secondary hover:bg-opacity-5'}`}
                        onClick={() => switchTab('register')}
                    >
                        Register
                        {activeTab === 'register' && (
                            <span className="absolute bottom-0 left-[20%] w-[60%] h-[3px] bg-secondary"></span>
                        )}
                    </div>
                </div>

                {/* Forms container */}
                <div className="p-8 relative min-h-[300px]">
                    {/* Login form */}
                    <form
                        className={`${activeTab === 'login' ? 'block' : 'hidden'}`}
                        onSubmit={handleLoginSubmit(onLogin)}
                    >
                        <FormField
                            id="username"
                            label="Username"
                            placeholder="Enter your username"
                            icon={<FontAwesomeIcon icon={faUser} className="text-gray-400"/>}
                            register={registerLoginField}
                            errors={loginErrors}
                            required
                        />

                        <div className="mb-6">
                            <label htmlFor="password" className="block font-medium mb-2 text-primary">
                                Password <span className="text-red-500">*</span>
                            </label>
                            <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                  <FontAwesomeIcon icon={faLock}/>
                </span>
                                <input
                                    type={showLoginPassword ? "text" : "password"}
                                    id="password"
                                    className={`w-full py-3 pl-10 pr-10 border ${loginErrors.password ? 'border-red-500' : 'border-gray-200'} 
                    rounded-lg text-base transition-all focus:outline-none focus:border-secondary 
                    focus:ring-2 focus:ring-secondary focus:ring-opacity-20`}
                                    placeholder="Enter your password"
                                    {...registerLoginField('password', {required: 'Password is required'})}
                                />
                                <button
                                    type="button"
                                    className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-secondary"
                                    onClick={() => setShowLoginPassword(!showLoginPassword)}
                                >
                                    <FontAwesomeIcon icon={showLoginPassword ? faEyeSlash : faEye}/>
                                </button>
                            </div>
                            {loginErrors.password && (
                                <p className="text-red-500 text-sm mt-1">{loginErrors.password.message}</p>
                            )}
                        </div>

                        <div className="flex items-center mb-6">
                            <input
                                type="checkbox"
                                id="remember-me"
                                className="w-5 h-5 mr-3 accent-secondary"
                                {...registerLoginField('rememberMe')}
                            />
                            <label htmlFor="remember-me">Remember me</label>
                        </div>

                        <a href="#" className="block text-right mb-6 text-primary text-sm hover:underline">
                            Forgot password?
                        </a>

                        <button
                            type="submit"
                            className="w-full py-3 px-6 rounded-lg bg-secondary text-white font-semibold
                transition-all duration-300 hover:bg-opacity-90 hover:-translate-y-[2px] hover:shadow-md"
                            disabled={isLoginSubmitting}
                        >
                            {isLoginSubmitting ? 'Signing In...' : 'Sign In'}
                        </button>
                    </form>

                    {/* Registration form */}
                    <form
                        className={`${activeTab === 'register' ? 'block' : 'hidden'}`}
                        onSubmit={handleRegisterSubmit(onRegister)}
                    >
                        <FormField
                            id="username"
                            label="Username"
                            placeholder="Create a username"
                            icon={<FontAwesomeIcon icon={faUser} className="text-gray-400"/>}
                            register={registerRegisterField}
                            errors={registerErrors}
                            required
                        />

                        <FormField
                            id="email"
                            label="Email"
                            type="email"
                            placeholder="Enter your email"
                            icon={<FontAwesomeIcon icon={faEnvelope} className="text-gray-400"/>}
                            register={registerRegisterField}
                            errors={registerErrors}
                            required
                        />

                        <div className="mb-6">
                            <label htmlFor="register-password" className="block font-medium mb-2 text-primary">
                                Password <span className="text-red-500">*</span>
                            </label>
                            <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                  <FontAwesomeIcon icon={faLock}/>
                </span>
                                <input
                                    type={showRegisterPassword ? "text" : "password"}
                                    id="register-password"
                                    className={`w-full py-3 pl-10 pr-10 border ${registerErrors.password ? 'border-red-500' : 'border-gray-200'} 
                    rounded-lg text-base transition-all focus:outline-none focus:border-secondary 
                    focus:ring-2 focus:ring-secondary focus:ring-opacity-20`}
                                    placeholder="Create a password"
                                    {...registerRegisterField('password', {
                                        required: 'Password is required',
                                        minLength: {
                                            value: 8,
                                            message: 'Password must be at least 8 characters'
                                        },
                                        validate: {
                                            hasUppercase: v => /[A-Z]/.test(v) || 'Must contain uppercase letter',
                                            hasNumber: v => /[0-9]/.test(v) || 'Must contain a number',
                                            hasSpecial: v => /[^A-Za-z0-9]/.test(v) || 'Must contain a special character'
                                        }
                                    })}
                                />
                                <button
                                    type="button"
                                    className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-secondary"
                                    onClick={() => setShowRegisterPassword(!showRegisterPassword)}
                                >
                                    <FontAwesomeIcon icon={showRegisterPassword ? faEyeSlash : faEye}/>
                                </button>
                            </div>
                            {registerErrors.password && (
                                <p className="text-red-500 text-sm mt-1">{registerErrors.password.message}</p>
                            )}

                            {/* Password strength meter */}
                            <PasswordStrengthMeter password={watchPassword}/>
                        </div>

                        <div className="mb-6">
                            <label htmlFor="confirmPassword" className="block font-medium mb-2 text-primary">
                                Confirm Password <span className="text-red-500">*</span>
                            </label>
                            <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                  <FontAwesomeIcon icon={faLock}/>
                </span>
                                <input
                                    type={showConfirmPassword ? "text" : "password"}
                                    id="confirmPassword"
                                    className={`w-full py-3 pl-10 pr-10 border ${registerErrors.confirmPassword ? 'border-red-500' : 'border-gray-200'} 
                    rounded-lg text-base transition-all focus:outline-none focus:border-secondary 
                    focus:ring-2 focus:ring-secondary focus:ring-opacity-20`}
                                    placeholder="Confirm your password"
                                    {...registerRegisterField('confirmPassword', {
                                        required: 'Please confirm your password',
                                        validate: value => value === getValues('password') || 'Passwords do not match'
                                    })}
                                />
                                <button
                                    type="button"
                                    className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-secondary"
                                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                >
                                    <FontAwesomeIcon icon={showConfirmPassword ? faEyeSlash : faEye}/>
                                </button>
                            </div>
                            {registerErrors.confirmPassword && (
                                <p className="text-red-500 text-sm mt-1">{registerErrors.confirmPassword.message}</p>
                            )}
                        </div>

                        <FormField
                            id="firstName"
                            label="First Name"
                            placeholder="Enter your first name"
                            icon={<FontAwesomeIcon icon={faUser} className="text-gray-400"/>}
                            register={registerRegisterField}
                            errors={registerErrors}
                            required
                        />

                        <FormField
                            id="lastName"
                            label="Last Name"
                            placeholder="Enter your last name (optional)"
                            icon={<FontAwesomeIcon icon={faUser} className="text-gray-400"/>}
                            register={registerRegisterField}
                            errors={registerErrors}
                        />

                        <button
                            type="submit"
                            className="w-full py-3 px-6 rounded-lg bg-secondary text-white font-semibold
                transition-all duration-300 hover:bg-opacity-90 hover:-translate-y-[2px] hover:shadow-md"
                            disabled={isRegisterSubmitting}
                        >
                            {isRegisterSubmitting ? 'Creating Account...' : 'Create Account'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

AuthTemplate.propTypes = {
    initialTab: PropTypes.oneOf(['login', 'register'])
};

export default AuthTemplate;