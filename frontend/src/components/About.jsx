import React from 'react';
import { Card, CardContent } from './ui/card';
import { Star, Clock, Heart, Award } from 'lucide-react';

const About = () => {
  const features = [
    {
      icon: <Heart className="h-8 w-8 text-black" />,
      title: "Frisch & Authentisch",
      description: "Alle Gerichte werden täglich frisch zubereitet mit authentischen Rezepten und Zutaten aus Asien."
    },
    {
      icon: <Award className="h-8 w-8 text-black" />,
      title: "Günstige Preise",
      description: "Erstklassige asiatische Küche zu erschwinglichen Preisen - ohne Kompromisse bei der Qualität."
    },
    {
      icon: <Clock className="h-8 w-8 text-black" />,
      title: "Schneller Takeaway",
      description: "Bestellen Sie online und holen Sie Ihr Essen in 15-30 Minuten ab. Perfekt für unterwegs."
    },
    {
      icon: <Star className="h-8 w-8 text-black" />,
      title: "Vielfältige Auswahl",
      description: "Von Thai-Currys bis zu chinesischen Klassikern - entdecken Sie die Vielfalt Asiens."
    }
  ];

  return (
    <section id="about" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Content */}
          <div className="space-y-8">
            <div className="space-y-6">
              <h2 
                className="text-4xl md:text-5xl font-bold text-black leading-tight"
                style={{ fontFamily: 'var(--font-serif)' }}
              >
                Willkommen bei Tantawan
              </h2>
              <p className="text-lg text-gray-600 leading-relaxed">
                Seit der Eröffnung in Frauenfeld verwöhnen wir unsere Gäste mit authentischer 
                asiatischer Küche. Unser Name "Tantawan" steht für Qualität, Frische und 
                erschwinglichen Genuss.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                Wir kombinieren traditionelle Kochkunst mit modernem Service. Bestellen Sie 
                einfach online und holen Sie Ihr frisch zubereitetes Essen ab - schnell, 
                bequem und immer köstlich.
              </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-black mb-2">1000+</div>
                <div className="text-sm text-gray-600 uppercase tracking-wide">Zufriedene Kunden</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-black mb-2">15-30</div>
                <div className="text-sm text-gray-600 uppercase tracking-wide">Min Zubereitungszeit</div>
              </div>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
                <CardContent className="p-6 space-y-4">
                  <div className="flex items-center justify-center w-16 h-16 bg-[#ECEC75] rounded-2xl mx-auto group-hover:scale-110 transition-transform duration-300">
                    {feature.icon}
                  </div>
                  <div className="text-center space-y-2">
                    <h3 className="text-lg font-bold text-black">{feature.title}</h3>
                    <p className="text-sm text-gray-600 leading-relaxed">{feature.description}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;