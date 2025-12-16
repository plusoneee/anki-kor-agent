import React from 'react';

/**
 * Glass Card Component
 * Main container with glassmorphism effect
 * Inspired by Arc Browser's translucent surfaces
 */
export const GlassCard = ({
  children,
  variant = 'default',
  className = '',
  hover = true,
}) => {
  const variantStyles = {
    default: 'bg-white/70',
    subtle: 'bg-white/60',
    emphasis: 'bg-white/75',
  };

  return (
    <div
      className={`
        ${variantStyles[variant]}
        backdrop-blur-glass-lg
        border border-white/30
        rounded-glass-lg
        shadow-glass-md
        p-8
        transition-all duration-500 ease-out
        ${hover ? 'hover:bg-white/75 hover:shadow-glass-lg hover:-translate-y-0.5' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  );
};

/**
 * Glass Button Component
 * Interactive button with smooth glassmorphism effects
 */
export const GlassButton = ({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
  type = 'button',
  className = '',
  fullWidth = false,
}) => {
  const variantStyles = {
    primary: `
      bg-gradient-to-br from-glass-indigo-400/60 to-glass-indigo-500/60
      hover:from-glass-indigo-400/70 hover:to-glass-indigo-500/70
      text-white font-semibold
      shadow-glass-md hover:shadow-glass-glow
    `,
    secondary: `
      bg-white/50
      hover:bg-white/65
      text-glass-text-primary font-medium
      shadow-glass-sm hover:shadow-glass-md
    `,
    accent: `
      bg-gradient-to-br from-glass-rose-300/60 to-glass-rose-400/60
      hover:from-glass-rose-300/70 hover:to-glass-rose-400/70
      text-white font-semibold
      shadow-glass-md hover:shadow-glass-glow-rose
    `,
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`
        ${variantStyles[variant]}
        backdrop-blur-glass-md
        border border-white/30
        rounded-glass-xl
        px-6 py-3
        transition-all duration-300 ease-out
        ${fullWidth ? 'w-full' : ''}
        ${disabled
          ? 'opacity-50 cursor-not-allowed'
          : 'hover:-translate-y-0.5 active:translate-y-0'
        }
        ${className}
      `}
    >
      {children}
    </button>
  );
};

/**
 * Glass Input Component
 * Text input with glassmorphism styling
 */
export const GlassInput = React.forwardRef(({
  value,
  onChange,
  placeholder,
  type = 'text',
  disabled = false,
  className = '',
  id,
}, ref) => {
  return (
    <input
      ref={ref}
      id={id}
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      disabled={disabled}
      className={`
        w-full
        bg-white/60
        backdrop-blur-glass-sm
        border border-white/40
        rounded-glass-md
        px-4 py-3
        text-glass-text-primary
        placeholder-glass-text-muted/60
        shadow-[inset_0_2px_8px_rgba(0,0,0,0.03)]
        transition-all duration-300 ease
        focus:bg-white/75
        focus:border-glass-indigo-300/40
        focus:shadow-[0_0_0_3px_rgba(139,92,246,0.1)]
        focus:outline-none
        disabled:opacity-50 disabled:cursor-not-allowed
        ${className}
      `}
      style={{ fontSize: '16px' }}
    />
  );
});

GlassInput.displayName = 'GlassInput';

/**
 * Glass Floating Element
 * Decorative floating element for visual interest
 */
export const GlassFloatingElement = ({
  size = 'md',
  color = 'indigo',
  position = 'top-right',
  className = '',
}) => {
  const sizeMap = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24',
    lg: 'w-32 h-32',
  };

  const colorMap = {
    indigo: 'bg-gradient-to-br from-glass-indigo-300/20 to-glass-indigo-400/20',
    rose: 'bg-gradient-to-br from-glass-rose-300/20 to-glass-rose-400/20',
    lavender: 'bg-glass-lavender/20',
  };

  const positionMap = {
    'top-right': 'absolute -top-4 -right-4',
    'top-left': 'absolute -top-4 -left-4',
    'bottom-right': 'absolute -bottom-4 -right-4',
    'bottom-left': 'absolute -bottom-4 -left-4',
  };

  return (
    <div
      className={`
        ${sizeMap[size]}
        ${colorMap[color]}
        ${positionMap[position]}
        rounded-full
        backdrop-blur-glass-md
        border border-white/20
        animate-float-slow
        pointer-events-none
        ${className}
      `}
      aria-hidden="true"
    />
  );
};

/**
 * Glass Badge Component
 * Small badge for stats or labels
 */
export const GlassBadge = ({
  children,
  variant = 'default',
  className = '',
}) => {
  const variantStyles = {
    default: 'bg-white/50 text-glass-text-secondary',
    success: 'bg-gradient-to-br from-green-400/40 to-green-500/40 text-green-900',
    warning: 'bg-gradient-to-br from-amber-400/40 to-amber-500/40 text-amber-900',
    info: 'bg-gradient-to-br from-glass-indigo-300/40 to-glass-indigo-400/40 text-indigo-900',
  };

  return (
    <span
      className={`
        ${variantStyles[variant]}
        backdrop-blur-glass-sm
        border border-white/30
        rounded-glass-md
        px-4 py-2
        text-sm font-medium
        inline-flex items-center
        shadow-glass-sm
        ${className}
      `}
    >
      {children}
    </span>
  );
};

/**
 * Glass Progress Bar
 * Progress indicator with glassmorphism styling
 */
export const GlassProgress = ({
  value,
  max = 100,
  color = 'indigo',
  className = '',
}) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const colorMap = {
    indigo: 'bg-gradient-to-r from-glass-indigo-400 to-glass-indigo-500',
    rose: 'bg-gradient-to-r from-glass-rose-400 to-glass-rose-500',
    success: 'bg-gradient-to-r from-green-400 to-green-500',
  };

  return (
    <div
      className={`
        w-full h-2
        bg-white/40
        backdrop-blur-glass-sm
        rounded-glass-sm
        border border-white/30
        overflow-hidden
        ${className}
      `}
    >
      <div
        className={`
          h-full
          ${colorMap[color]}
          transition-all duration-700 ease-out
          shadow-[0_0_12px_rgba(139,92,246,0.3)]
        `}
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
};

/**
 * Glass Notification/Alert Component
 * For displaying success, error, or info messages
 */
export const GlassNotification = ({
  children,
  type = 'info',
  onClose,
  className = '',
}) => {
  const typeStyles = {
    success: {
      bg: 'bg-gradient-to-br from-green-50/80 to-green-100/80',
      border: 'border-green-300/40',
      icon: '✓',
      iconColor: 'text-green-600',
    },
    error: {
      bg: 'bg-gradient-to-br from-red-50/80 to-red-100/80',
      border: 'border-red-300/40',
      icon: '✗',
      iconColor: 'text-red-600',
    },
    warning: {
      bg: 'bg-gradient-to-br from-amber-50/80 to-amber-100/80',
      border: 'border-amber-300/40',
      icon: '!',
      iconColor: 'text-amber-600',
    },
    info: {
      bg: 'bg-gradient-to-br from-glass-indigo-50/80 to-glass-indigo-100/80',
      border: 'border-glass-indigo-300/40',
      icon: 'i',
      iconColor: 'text-glass-indigo-600',
    },
  };

  const style = typeStyles[type];

  return (
    <div
      className={`
        ${style.bg}
        ${style.border}
        backdrop-blur-glass-md
        border
        rounded-glass-lg
        p-4
        shadow-glass-md
        animate-slide-up
        relative
        ${className}
      `}
    >
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-glass-text-secondary hover:text-glass-text-primary transition-colors duration-200 text-xl leading-none w-6 h-6 flex items-center justify-center"
          aria-label="Close"
        >
          ×
        </button>
      )}
      <div className="flex items-start gap-3">
        <span className={`${style.iconColor} font-bold text-lg flex-shrink-0`}>
          {style.icon}
        </span>
        <div className="flex-1">{children}</div>
      </div>
    </div>
  );
};
