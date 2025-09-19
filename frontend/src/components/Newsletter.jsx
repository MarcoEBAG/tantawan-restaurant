import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent } from './ui/card';
import { Mail, Check, Gift, Clock, Star, Loader2 } from 'lucide-react';
import { newsletterAPI } from '../services/api';
import { toast } from 'sonner';

const Newsletter = () => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [subscriptionCount, setSubscriptionCount] = useState(500); // Default fallback

  // Fetch subscription count on component mount
  useEffect(() => {
    const fetchSubscriptionCount = async () => {
      try {
        const data = await newsletterAPI.getSubscriptionCount();
        setSubscriptionCount(data.active_subscriptions);
      } catch (error) {
        console.error('Error fetching subscription count:', error);
        // Keep default value on error
      }
    };

    fetchSubscriptionCount();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email.trim()) {
      toast.error('Bitte geben Sie Ihre E-Mail-Adresse ein');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      toast.error('Bitte geben Sie eine gültige E-Mail-Adresse ein');
      return;
    }

    setIsLoading(true);

    try {
      const response = await newsletterAPI.subscribe(email);
      
      console.log('Newsletter subscription successful:', response);
      
      setIsSubscribed(true);
      toast.success('🎉 Erfolgreich angemeldet! Willkommen im Tantawan Newsletter!');
      setEmail('');
      
      // Update subscription count
      setSubscriptionCount(prev => prev + 1);
      
    } catch (error) {
      console.error('Newsletter subscription failed:', error);
      
      if (error.message.includes('already subscribed')) {
        toast.error('Diese E-Mail-Adresse ist bereits für unseren Newsletter angemeldet.');
      } else {
        toast.error(error.message || 'Anmeldung fehlgeschlagen. Versuchen Sie es später erneut.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const benefits = [
    {
      icon: <Gift className="h-5 w-5 text-black" />,
      title: "Exklusive Angebote",
      description: "Erhalten Sie spezielle Rabatte und Aktionen nur für Newsletter-Abonnenten"
    },
    {
      icon: <Clock className="h-5 w-5 text-black" />,
      title: "Neue Gerichte zuerst",
      description: "Erfahren Sie als Erster von neuen Gerichten und saisonalen Spezialitäten"
    },
    {
      icon: <Star className="h-5 w-5 text-black" />,
      title: "Insider-Tipps",
      description: "Bekommen Sie Kochtipps und Geschichten hinter unseren authentischen Rezepten"
    }
  ];

  if (isSubscribed) {
    return (
      <section id="newsletter" className="py-20 bg-gradient-to-br from-[#ECEC75] to-[#e6e67c]">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Card className="border-0 shadow-2xl bg-white/90 backdrop-blur-sm">
            <CardContent className="p-12">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Check className="h-10 w-10 text-green-600" />
              </div>
              <h2 
                className="text-3xl md:text-4xl font-bold text-black mb-4"
                style={{ fontFamily: 'var(--font-serif)' }}
              >
                Willkommen im Tantawan Newsletter!
              </h2>
              <p className="text-lg text-gray-600 mb-6">
                Vielen Dank für Ihre Anmeldung! Sie erhalten in Kürze eine Bestätigungs-E-Mail 
                und werden über alle Neuigkeiten und Angebote informiert.
              </p>
              <Button
                onClick={() => setIsSubscribed(false)}
                variant="outline"
                className="border-black text-black hover:bg-black hover:text-white"
              >
                Weitere E-Mail hinzufügen
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>
    );
  }

  return (
    <section id="newsletter" className="py-20 bg-gradient-to-br from-[#ECEC75] to-[#e6e67c]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <div className="space-y-8">
            <div className="space-y-6">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-black rounded-lg flex items-center justify-center">
                  <Mail className="h-6 w-6 text-white" />
                </div>
                <h2 
                  className="text-4xl md:text-5xl font-bold text-black leading-tight"
                  style={{ fontFamily: 'var(--font-serif)' }}
                >
                  Newsletter
                </h2>
              </div>
              
              <p className="text-xl text-gray-700 leading-relaxed">
                Bleiben Sie auf dem Laufenden mit unserem Newsletter und verpassen Sie 
                keine Neuigkeiten, Angebote oder kulinarischen Tipps von Tantawan!
              </p>
            </div>

            {/* Benefits */}
            <div className="space-y-4">
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-start space-x-4">
                  <div className="flex items-center justify-center w-10 h-10 bg-white rounded-lg shadow-sm flex-shrink-0">
                    {benefit.icon}
                  </div>
                  <div>
                    <h3 className="font-semibold text-black mb-1">{benefit.title}</h3>
                    <p className="text-gray-600 text-sm leading-relaxed">{benefit.description}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Newsletter Form */}
            <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
              <CardContent className="p-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-semibold text-black mb-2">
                        E-Mail-Adresse *
                      </label>
                      <Input
                        type="email"
                        placeholder="ihre.email@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="h-12 text-lg border-2 border-gray-200 focus:border-black transition-colors duration-200"
                        disabled={isLoading}
                      />
                    </div>
                  </div>

                  <Button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-black text-white hover:bg-gray-800 text-lg py-6 font-semibold transition-all duration-200 hover:transform hover:-translate-y-0.5 hover:shadow-lg"
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center space-x-2">
                        <Loader2 className="h-5 w-5 animate-spin" />
                        <span>Anmeldung läuft...</span>
                      </div>
                    ) : (
                      <div className="flex items-center justify-center space-x-2">
                        <Mail className="h-5 w-5" />
                        <span>Jetzt Anmelden</span>
                      </div>
                    )}
                  </Button>

                  <p className="text-xs text-gray-500 text-center leading-relaxed">
                    Mit der Anmeldung stimmen Sie unseren Datenschutzbestimmungen zu. 
                    Sie können sich jederzeit wieder abmelden.
                  </p>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Visual Element */}
          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden shadow-2xl">
              <img
                src="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=600&fit=crop&crop=center"
                alt="Newsletter Anmeldung - Frische asiatische Küche"
                className="w-full h-[500px] object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>
              
              {/* Overlay Content */}
              <div className="absolute bottom-8 left-8 right-8 text-white">
                <h3 className="text-2xl font-bold mb-2" style={{ fontFamily: 'var(--font-serif)' }}>
                  Kulinarische Neuigkeiten
                </h3>
                <p className="text-white/90 text-sm leading-relaxed">
                  Erfahren Sie mehr über die Geheimnisse der asiatischen Küche 
                  und unsere frischen Zutaten direkt in Ihrem Postfach.
                </p>
              </div>
            </div>

            {/* Floating Stats */}
            <div className="absolute -top-6 -right-6 bg-white rounded-lg shadow-lg p-6 max-w-xs">
              <div className="text-center">
                <p className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
                  Newsletter Abonnenten
                </p>
                <p className="text-3xl font-bold text-black mt-1">{subscriptionCount}+</p>
                <p className="text-sm text-gray-500 mt-1">
                  Zufriedene Leser
                </p>
              </div>
            </div>

            <div className="absolute -bottom-6 -left-6 bg-[#ECEC75] rounded-lg shadow-lg p-6 max-w-xs">
              <div className="text-center">
                <p className="text-sm font-semibold text-gray-700 uppercase tracking-wide">
                  Wöchentlicher Newsletter
                </p>
                <p className="text-2xl font-bold text-black mt-1">Jeden Freitag</p>
                <p className="text-sm text-gray-600 mt-1">
                  Pünktlich um 10:00 Uhr
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Newsletter;