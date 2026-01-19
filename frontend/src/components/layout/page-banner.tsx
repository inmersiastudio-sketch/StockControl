import { cn } from '@/lib/utils';

export interface PageBannerProps {
  title: string;
  description?: string;
  icon?: React.ReactNode;
  color?: 'blue' | 'green' | 'orange' | 'purple' | 'indigo';
}

const colorClasses = {
  blue: 'bg-primary-50 text-primary-700 border-primary-200',
  green: 'bg-success-50 text-success-700 border-success-200',
  orange: 'bg-warning-50 text-warning-700 border-warning-200',
  purple: 'bg-purple-50 text-purple-700 border-purple-200',
  indigo: 'bg-indigo-50 text-indigo-700 border-indigo-200',
};

export function PageBanner({ title, description, icon, color = 'blue' }: PageBannerProps) {
  return (
    <div className={cn('rounded-lg p-4 mb-6 border', colorClasses[color])}>
      <div className="flex items-center gap-3">
        {icon && <div className="text-2xl">{icon}</div>}
        <div>
          <h1 className="text-xl font-bold">{title}</h1>
          {description && <p className="text-sm italic opacity-80">{description}</p>}
        </div>
      </div>
    </div>
  );
}
