import React from 'react';
import { MapPin, Phone, Clock, Mail, Facebook, Instagram } from 'lucide-react';
import { restaurantInfo } from '../data/mockData';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Restaurant Info */}
          <div className="space-y-4">
            <h3 
              className="text-2xl font-bold text-[#ECEC75]"
              style={{ fontFamily: 'var(--font-serif)' }}
            >
              Tantawan
            </h3>
            <p className="text-gray-300 text-sm leading-relaxed">
              Authentische asiatische Küche in Frauenfeld. Frisch gekocht, 
              günstig und extrem fein - perfekt für Takeaway.
            </p>
            <div className="flex space-x-4">
              <div className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-[#ECEC75] hover:text-black transition-colors duration-200 cursor-pointer">
                <Facebook className="h-5 w-5" />
              </div>
              <div className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-[#ECEC75] hover:text-black transition-colors duration-200 cursor-pointer">
                <Instagram className="h-5 w-5" />
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-white">Quick Links</h4>
            <ul className="space-y-2">
              {[
                { name: 'Home', href: '#home' },
                { name: 'Speisekarte', href: '#menu' },
                { name: 'Über uns', href: '#about' },
                { name: 'Newsletter', href: '#newsletter' },
                { name: 'Kontakt', href: '#contact' }
              ].map((link) => (
                <li key={link.name}>
                  <a 
                    href={link.href}
                    className="text-gray-300 hover:text-[#ECEC75] transition-colors duration-200 text-sm"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-white">Kontakt</h4>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <MapPin className="h-4 w-4 text-[#ECEC75] flex-shrink-0" />
                <span className="text-gray-300 text-sm">{restaurantInfo.address}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Phone className="h-4 w-4 text-[#ECEC75] flex-shrink-0" />
                <span className="text-gray-300 text-sm">{restaurantInfo.phone}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="h-4 w-4 text-[#ECEC75] flex-shrink-0" />
                <span className="text-gray-300 text-sm">{restaurantInfo.email}</span>
              </div>
            </div>
          </div>

          {/* Newsletter Signup */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-white">Newsletter</h4>
            <p className="text-gray-300 text-sm leading-relaxed">
              Bleiben Sie informiert über neue Gerichte und Angebote!
            </p>
            <a 
              href="#newsletter"
              className="inline-block bg-[#ECEC75] text-black px-4 py-2 rounded-lg font-semibold text-sm hover:bg-yellow-400 transition-colors duration-200"
            >
              Jetzt Anmelden
            </a>
            <div className="space-y-1 text-xs text-gray-400">
              <p>📧 Wöchentlich freitags</p>
              <p>🎁 Exklusive Angebote</p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-gray-400 text-sm">
              © {currentYear} Tantawan Restaurant. Alle Rechte vorbehalten.
            </div>
            <div className="flex space-x-6 text-sm">
              <a href="#" className="text-gray-400 hover:text-[#ECEC75] transition-colors duration-200">
                Datenschutz
              </a>
              <a href="#" className="text-gray-400 hover:text-[#ECEC75] transition-colors duration-200">
                AGB
              </a>
              <a href="#" className="text-gray-400 hover:text-[#ECEC75] transition-colors duration-200">
                Impressum
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;