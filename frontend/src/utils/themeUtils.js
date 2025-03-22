/**
 * Utility functions and constants for theme handling
 * Provides static classes for Tailwind compatibility
 */

// Theme classes for various components with common patterns
export const themeClasses = {
  // Antenna theme
  antenna: {
    text: "text-antenna",
    bg: "bg-antenna",
    bgOpacity: {
      5: "bg-antenna bg-opacity-5",
      10: "bg-antenna bg-opacity-10"
    },
    border: "border-antenna",
    borderLight: "border-antenna-light",
    borderTop: "border-t-antenna",
    hover: {
      bg: "hover:bg-antenna",
      text: "hover:text-antenna"
    },
    combined: {
      actionButton: "bg-white text-antenna border-2 border-antenna hover:bg-antenna hover:text-white",
      activeTab: "text-antenna border-b-3 border-antenna bg-antenna bg-opacity-5"
    }
  },

  // Video theme
  video: {
    text: "text-video",
    bg: "bg-video",
    bgOpacity: {
      5: "bg-video bg-opacity-5",
      10: "bg-video bg-opacity-10"
    },
    border: "border-video",
    borderLight: "border-video-light",
    borderTop: "border-t-video",
    hover: {
      bg: "hover:bg-video",
      text: "hover:text-video"
    },
    combined: {
      actionButton: "bg-white text-video border-2 border-video hover:bg-video hover:text-white",
      activeTab: "text-video border-b-3 border-video bg-video bg-opacity-5"
    }
  },

  // Frame theme
  frame: {
    text: "text-frame",
    bg: "bg-frame",
    bgOpacity: {
      5: "bg-frame bg-opacity-5",
      10: "bg-frame bg-opacity-10"
    },
    border: "border-frame",
    borderTop: "border-t-frame",
    hover: {
      bg: "hover:bg-frame",
      text: "hover:text-frame"
    },
    combined: {
      actionButton: "bg-white text-frame border-2 border-frame hover:bg-frame hover:text-white",
      activeTab: "text-frame border-b-3 border-frame bg-frame bg-opacity-5"
    }
  },

  // Propulsion theme
  propulsion: {
    text: "text-propulsion",
    bg: "bg-propulsion",
    bgOpacity: {
      5: "bg-propulsion bg-opacity-5",
      10: "bg-propulsion bg-opacity-10"
    },
    border: "border-propulsion",
    borderTop: "border-t-propulsion",
    hover: {
      bg: "hover:bg-propulsion",
      text: "hover:text-propulsion"
    },
    combined: {
      actionButton: "bg-white text-propulsion border-2 border-propulsion hover:bg-propulsion hover:text-white",
      activeTab: "text-propulsion border-b-3 border-propulsion bg-propulsion bg-opacity-5"
    }
  },

  // Control theme
  control: {
    text: "text-control",
    bg: "bg-control",
    bgOpacity: {
      5: "bg-control bg-opacity-5",
      10: "bg-control bg-opacity-10"
    },
    border: "border-control",
    borderTop: "border-t-control",
    hover: {
      bg: "hover:bg-control",
      text: "hover:text-control"
    },
    combined: {
      actionButton: "bg-white text-control border-2 border-control hover:bg-control hover:text-white",
      activeTab: "text-control border-b-3 border-control bg-control bg-opacity-5"
    }
  },

  // Drone theme
  drone: {
    text: "text-drone",
    bg: "bg-drone",
    bgOpacity: {
      5: "bg-drone bg-opacity-5",
      10: "bg-drone bg-opacity-10"
    },
    border: "border-drone",
    borderLight: "border-drone-light",
    borderTop: "border-t-drone",
    hover: {
      bg: "hover:bg-drone",
      text: "hover:text-drone"
    },
    combined: {
      actionButton: "bg-white text-drone border-2 border-drone hover:bg-drone hover:text-white",
      activeTab: "text-drone border-b-3 border-drone bg-drone bg-opacity-5"
    }
  },

  // Primary theme (default)
  primary: {
    text: "text-primary",
    bg: "bg-primary",
    bgOpacity: {
      5: "bg-primary bg-opacity-5",
      10: "bg-primary bg-opacity-10"
    },
    border: "border-primary",
    borderTop: "border-t-primary",
    hover: {
      bg: "hover:bg-primary",
      text: "hover:text-primary"
    },
    combined: {
      actionButton: "bg-white text-primary border-2 border-primary hover:bg-primary hover:text-white",
      activeTab: "text-primary border-b-3 border-primary bg-primary bg-opacity-5"
    }
  }
};

/**
 * Get common class patterns for a theme
 *
 * @param {string} themeName - The theme name
 * @param {string} pattern - Pattern type (e.g., 'button', 'card', etc.)
 * @returns {string} Tailwind classes for the specified theme and pattern
 */
export function getThemeClasses(themeName, pattern) {
  const theme = themeClasses[themeName] || themeClasses.primary;

  switch (pattern) {
    case 'actionButton':
      return theme.combined.actionButton;
    case 'activeTab':
      return theme.combined.activeTab;
    case 'borderAccent':
      return theme.borderTop;
    default:
      return '';
  }
}