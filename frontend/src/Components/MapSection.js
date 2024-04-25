import React from 'react';

function MapSection() {
    return (
        <div>
            <h2>Map Section</h2>
            <iframe
                title="map"
                width="100%"
                height="400"
                frameborder="0"
                scrolling="no"
                marginheight="0"
                marginwidth="0"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3132.5952262287827!2d-77.30518168468276!3d38.827446379576076!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89b64b1263d638a1%3A0xdf95a2cf61eb0b6b!2sGeorge%20Mason%20University!5e0!3m2!1sen!2sus!4v1585053057861!5m2!1sen!2sus">
            </iframe>
        </div>
    );
}
export default MapSection;