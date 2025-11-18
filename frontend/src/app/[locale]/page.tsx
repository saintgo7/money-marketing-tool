import { useTranslations } from 'next-intl';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import LanguageSwitcher from '@/components/LanguageSwitcher';

export default function HomePage() {
  const t = useTranslations();

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">{t('common.appName')}</h1>
          <div className="flex gap-4 items-center">
            <LanguageSwitcher />
            <Link href="/login">
              <Button variant="outline">{t('common.login')}</Button>
            </Link>
            <Link href="/signup">
              <Button>{t('common.signup')}</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-b from-blue-50 to-white">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">
            {t('home.hero.title')}{' '}
            <span className="text-blue-600">{t('home.hero.titleHighlight')}</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            {t('home.hero.description')}
          </p>
          <div className="flex gap-4 justify-center">
            <Button size="lg">{t('home.hero.startFreeTrial')}</Button>
            <Button size="lg" variant="outline">{t('home.hero.viewDemo')}</Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            {t('home.features.title')}
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="p-6 border rounded-lg">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold mb-2">
                {t('home.features.aiContent.title')}
              </h3>
              <p className="text-gray-600">
                {t('home.features.aiContent.description')}
              </p>
            </div>
            <div className="p-6 border rounded-lg">
              <div className="text-4xl mb-4">📱</div>
              <h3 className="text-xl font-semibold mb-2">
                {t('home.features.multiPlatform.title')}
              </h3>
              <p className="text-gray-600">
                {t('home.features.multiPlatform.description')}
              </p>
            </div>
            <div className="p-6 border rounded-lg">
              <div className="text-4xl mb-4">⏰</div>
              <h3 className="text-xl font-semibold mb-2">
                {t('home.features.smartScheduling.title')}
              </h3>
              <p className="text-gray-600">
                {t('home.features.smartScheduling.description')}
              </p>
            </div>
            <div className="p-6 border rounded-lg">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2">
                {t('home.features.analytics.title')}
              </h3>
              <p className="text-gray-600">
                {t('home.features.analytics.description')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">
            {t('home.pricing.title')}
          </h2>
          <p className="text-center text-gray-600 mb-12">
            {t('home.pricing.subtitle')}
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Free Plan */}
            <div className="bg-white p-8 rounded-lg border">
              <h3 className="text-2xl font-bold mb-2">{t('home.pricing.free.name')}</h3>
              <div className="text-4xl font-bold mb-4">
                {t('home.pricing.free.price')}
                <span className="text-lg text-gray-600">{t('home.pricing.free.period')}</span>
              </div>
              <ul className="space-y-3 mb-8">
                {(t.raw('home.pricing.free.features') as string[]).map((feature, i) => (
                  <li key={i} className="flex items-start">
                    <span className="mr-2">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <Button className="w-full" variant="outline">
                {t('home.pricing.selectPlan')}
              </Button>
            </div>

            {/* Starter Plan */}
            <div className="bg-white p-8 rounded-lg border-2 border-blue-500 relative">
              <div className="absolute top-0 right-0 bg-blue-500 text-white px-4 py-1 text-sm rounded-bl-lg">
                Popular
              </div>
              <h3 className="text-2xl font-bold mb-2">{t('home.pricing.starter.name')}</h3>
              <div className="text-4xl font-bold mb-4">
                {t('home.pricing.starter.price')}
                <span className="text-lg text-gray-600">{t('home.pricing.starter.period')}</span>
              </div>
              <ul className="space-y-3 mb-8">
                {(t.raw('home.pricing.starter.features') as string[]).map((feature, i) => (
                  <li key={i} className="flex items-start">
                    <span className="mr-2">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <Button className="w-full">
                {t('home.pricing.selectPlan')}
              </Button>
            </div>

            {/* Pro Plan */}
            <div className="bg-white p-8 rounded-lg border">
              <h3 className="text-2xl font-bold mb-2">{t('home.pricing.pro.name')}</h3>
              <div className="text-4xl font-bold mb-4">
                {t('home.pricing.pro.price')}
                <span className="text-lg text-gray-600">{t('home.pricing.pro.period')}</span>
              </div>
              <ul className="space-y-3 mb-8">
                {(t.raw('home.pricing.pro.features') as string[]).map((feature, i) => (
                  <li key={i} className="flex items-start">
                    <span className="mr-2">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <Button className="w-full" variant="outline">
                {t('home.pricing.selectPlan')}
              </Button>
            </div>

            {/* Agency Plan */}
            <div className="bg-white p-8 rounded-lg border">
              <h3 className="text-2xl font-bold mb-2">{t('home.pricing.agency.name')}</h3>
              <div className="text-4xl font-bold mb-4">
                {t('home.pricing.agency.price')}
                <span className="text-lg text-gray-600">{t('home.pricing.agency.period')}</span>
              </div>
              <ul className="space-y-3 mb-8">
                {(t.raw('home.pricing.agency.features') as string[]).map((feature, i) => (
                  <li key={i} className="flex items-start">
                    <span className="mr-2">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <Button className="w-full" variant="outline">
                {t('home.pricing.selectPlan')}
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">{t('home.cta.title')}</h2>
          <p className="text-xl text-gray-600 mb-8">
            {t('home.cta.description')}
          </p>
          <Button size="lg">{t('home.cta.button')}</Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 bg-gray-50">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>© 2025 {t('common.appName')}. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
