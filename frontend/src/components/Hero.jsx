import React from 'react';
import { Button } from './ui/button';
import { Clock, MapPin, Phone } from 'lucide-react';

const Hero = () => {
  const scrollToMenu = () => {
    document.getElementById('menu')?.scrollIntoView({ 
      behavior: 'smooth' 
    });
  };

  return (
    <section id="home" className="pt-16 bg-gradient-to-br from-[#ECEC75] to-[#e6e67c] min-h-screen flex items-center">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 
                className="text-5xl md:text-6xl lg:text-7xl font-bold text-black leading-tight"
                style={{ fontFamily: 'var(--font-serif)' }}
              >
                Tantawan
              </h1>
              <p className="text-xl md:text-2xl text-gray-700 font-medium">
                Authentische Asiatische Küche
              </p>
              <p className="text-lg text-gray-600 max-w-md">
                Frisch gekocht • Extrem fein • Günstige Preise
                <br />
                <span className="font-semibold">Jetzt online bestellen für Takeaway!</span>
              </p>
            </div>

            {/* Quick Info */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
              <div className="flex items-center space-x-2 text-gray-700">
                <MapPin className="h-4 w-4 text-black" />
                <span>Zürcherstrasse 232, Frauenfeld</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-700">
                <Clock className="h-4 w-4 text-black" />
                <span>11:00 - 21:30</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-700">
                <Phone className="h-4 w-4 text-black" />
                <span>+41 52 721 XX XX</span>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                size="lg" 
                className="bg-black text-white hover:bg-gray-800 text-lg px-8 py-6 rounded-lg font-semibold transition-all duration-200 hover:transform hover:-translate-y-0.5 hover:shadow-lg"
                onClick={scrollToMenu}
              >
                Jetzt Bestellen
              </Button>
              <Button 
                variant="outline" 
                size="lg"
                className="border-2 border-black text-black hover:bg-black hover:text-white text-lg px-8 py-6 rounded-lg font-semibold transition-all duration-200 hover:transform hover:-translate-y-0.5"
                onClick={() => document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Mehr Erfahren
              </Button>
            </div>
          </div>

          {/* Hero Image */}
          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden shadow-2xl transform hover:scale-105 transition-transform duration-300">
              <img
                src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=600&fit=crop&crop=center"
                alt="Delicious Asian cuisine at Tantawan restaurant"
                className="w-full h-[500px] object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
            </div>
            
            {/* Floating Info Card */}
            <div className="absolute -bottom-6 -left-6 bg-white rounded-lg shadow-lg p-6 max-w-xs">
              <div className="text-center">
                <p className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
                  Takeaway Service
                </p>
                <p className="text-2xl font-bold text-black mt-1">15-30 Min</p>
                <p className="text-sm text-gray-500 mt-1">
                  Schnelle Zubereitung
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;