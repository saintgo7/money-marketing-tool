import Link from "next/link";
import { ArrowRight, Sparkles, Calendar, BarChart3, Zap } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-8 h-8 text-blue-600" />
            <span className="text-2xl font-bold text-gray-900">Money Marketing Tool</span>
          </div>
          <div className="flex space-x-4">
            <Link
              href="/login"
              className="px-4 py-2 text-gray-700 hover:text-blue-600 transition"
            >
              Login
            </Link>
            <Link
              href="/signup"
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Get Started
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-6">
          AI-Powered Marketing
          <br />
          <span className="text-blue-600">On Autopilot</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Generate engaging content, schedule posts at optimal times, and analyze performance
          across all your social media platforms - all powered by AI.
        </p>
        <div className="flex justify-center space-x-4">
          <Link
            href="/signup"
            className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center space-x-2 text-lg"
          >
            <span>Start Free Trial</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            href="/demo"
            className="px-8 py-4 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition text-lg"
          >
            View Demo
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-12">Everything You Need to Succeed</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <FeatureCard
            icon={<Sparkles className="w-10 h-10 text-blue-600" />}
            title="AI Content Generation"
            description="Generate platform-optimized content with Claude AI in seconds"
          />
          <FeatureCard
            icon={<Calendar className="w-10 h-10 text-blue-600" />}
            title="Smart Scheduling"
            description="Post at optimal times based on your audience engagement data"
          />
          <FeatureCard
            icon={<BarChart3 className="w-10 h-10 text-blue-600" />}
            title="Performance Analytics"
            description="Track metrics across all platforms in one unified dashboard"
          />
          <FeatureCard
            icon={<Zap className="w-10 h-10 text-blue-600" />}
            title="Multi-Platform"
            description="Manage Instagram, Facebook, Twitter, LinkedIn, and more"
          />
        </div>
      </section>

      {/* Pricing Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-12">Simple, Transparent Pricing</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          <PricingCard
            tier="Free"
            price="$0"
            features={[
              "3 social accounts",
              "30 AI generations/month",
              "Basic scheduling",
              "Weekly reports",
            ]}
          />
          <PricingCard
            tier="Starter"
            price="$29"
            features={[
              "10 social accounts",
              "200 AI generations/month",
              "50 image generations",
              "Optimal timing",
              "Daily reports",
            ]}
            popular
          />
          <PricingCard
            tier="Pro"
            price="$79"
            features={[
              "25 social accounts",
              "Unlimited AI content",
              "200 image generations",
              "Team collaboration (5)",
              "API access",
            ]}
          />
          <PricingCard
            tier="Agency"
            price="$199"
            features={[
              "Unlimited accounts",
              "Client management",
              "White-label reports",
              "Priority support",
              "Dedicated manager",
            ]}
          />
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            © 2025 Money Marketing Tool. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function PricingCard({
  tier,
  price,
  features,
  popular = false,
}: {
  tier: string;
  price: string;
  features: string[];
  popular?: boolean;
}) {
  return (
    <div
      className={`p-6 rounded-lg border-2 ${
        popular
          ? "border-blue-600 shadow-lg scale-105"
          : "border-gray-200"
      } bg-white relative`}
    >
      {popular && (
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-blue-600 text-white px-3 py-1 rounded-full text-sm">
          Popular
        </div>
      )}
      <h3 className="text-2xl font-bold mb-2">{tier}</h3>
      <div className="mb-6">
        <span className="text-4xl font-bold">{price}</span>
        <span className="text-gray-600">/month</span>
      </div>
      <ul className="space-y-3 mb-6">
        {features.map((feature, i) => (
          <li key={i} className="flex items-start">
            <svg
              className="w-5 h-5 text-blue-600 mr-2 mt-0.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            <span className="text-gray-700">{feature}</span>
          </li>
        ))}
      </ul>
      <button
        className={`w-full py-3 rounded-lg font-semibold transition ${
          popular
            ? "bg-blue-600 text-white hover:bg-blue-700"
            : "bg-gray-100 text-gray-900 hover:bg-gray-200"
        }`}
      >
        Get Started
      </button>
    </div>
  );
}
