// Export all API services from a single entry point

// Export the base API functions
export * from './base';

// Export domain-specific API functions
export * as componentsApi from './components';
export * as dronesApi from './drones';
export * as authApi from './auth';
export * as usersApi from './users';
// export * as suggestionsApi from './suggestions';
export * as listsApi from './lists';

// You can add more domains as your application grows
