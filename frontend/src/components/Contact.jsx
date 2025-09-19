import React from 'react';
import { Card, CardContent } from './ui/card';
import { MapPin, Phone, Clock, Mail } from 'lucide-react';
import { restaurantInfo } from '../data/mockData';

const Contact = () => {
  const contactInfo = [
    {
      icon: <MapPin className="h-6 w-6 text-black" />,
      title: "Adresse",
      content: restaurantInfo.address,
      action: () => window.open(`https://maps.google.com/search/${encodeURIComponent(restaurantInfo.address)}`, '_blank')
    },
    {
      icon: <Phone className="h-6 w-6 text-black" />,
      title: "Telefon",
      content: restaurantInfo.phone,
      action: () => window.open(`tel:${restaurantInfo.phone}`)
    },
    {
      icon: <Mail className="h-6 w-6 text-black" />,
      title: "E-Mail",
      content: restaurantInfo.email,
      action: () => window.open(`mailto:${restaurantInfo.email}`)
    }
  ];

  const days = [
    { day: 'Montag', hours: restaurantInfo.openingHours.monday },
    { day: 'Dienstag', hours: restaurantInfo.openingHours.tuesday },
    { day: 'Mittwoch', hours: restaurantInfo.openingHours.wednesday },
    { day: 'Donnerstag', hours: restaurantInfo.openingHours.thursday },
    { day: 'Freitag', hours: restaurantInfo.openingHours.friday },
    { day: 'Samstag', hours: restaurantInfo.openingHours.saturday },
    { day: 'Sonntag', hours: restaurantInfo.openingHours.sunday }
  ];

  return (
    <section id="contact" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 
            className="text-4xl md:text-5xl font-bold text-black mb-6"
            style={{ fontFamily: 'var(--font-serif)' }}
          >
            Kontakt & Standort
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Besuchen Sie uns in Frauenfeld oder kontaktieren Sie uns für Fragen zu Ihren Bestellungen.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Information */}
          <div className="space-y-8">
            <div className="space-y-6">
              {contactInfo.map((info, index) => (
                <Card 
                  key={index} 
                  className="border-0 shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer group"
                  onClick={info.action}
                >
                  <CardContent className="p-6">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center justify-center w-12 h-12 bg-[#ECEC75] rounded-lg group-hover:scale-110 transition-transform duration-300">
                        {info.icon}
                      </div>
                      <div>
                        <h3 className="font-semibold text-black mb-1">{info.title}</h3>
                        <p className="text-gray-600">{info.content}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Opening Hours */}
            <Card className="border-0 shadow-md">
              <CardContent className="p-6">
                <div className="flex items-center space-x-4 mb-6">
                  <div className="flex items-center justify-center w-12 h-12 bg-[#ECEC75] rounded-lg">
                    <Clock className="h-6 w-6 text-black" />
                  </div>
                  <h3 className="text-xl font-bold text-black">Öffnungszeiten</h3>
                </div>
                
                <div className="space-y-3">
                  {days.map((day, index) => (
                    <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
                      <span className="font-medium text-gray-900">{day.day}</span>
                      <span className="text-gray-600">{day.hours}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Map */}
          <div className="space-y-6">
            <Card className="border-0 shadow-md overflow-hidden">
              <div className="aspect-w-16 aspect-h-12">
                <iframe
                  src={`https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dO4W0c_0qY5_hQ&q=${encodeURIComponent(restaurantInfo.address)}`}
                  width="100%"
                  height="400"
                  style={{ border: 0 }}
                  allowFullScreen=""
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  className="rounded-lg"
                  title="Tantawan Restaurant Location"
                ></iframe>
              </div>
            </Card>

            {/* Additional Info */}
            <Card className="border-0 shadow-md bg-[#ECEC75]">
              <CardContent className="p-6 text-center">
                <h3 className="text-xl font-bold text-black mb-3">Takeaway Service</h3>
                <p className="text-gray-700 mb-4">
                  Bestellen Sie online und holen Sie Ihr Essen einfach ab. 
                  Kein Lieferservice - aber immer frisch zubereitet!
                </p>
                <div className="text-sm text-gray-600">
                  <p className="font-semibold">Zubereitungszeit: 15-30 Minuten</p>
                  <p>Je nach Bestellmenge und Tageszeit</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;