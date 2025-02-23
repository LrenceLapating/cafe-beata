<template>
  <div class="coffee-container">
    <header class="header">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">

      <div class="logo" @click="scrollToTop">UIC Café Beàta</div>
      <nav class="nav-links">
        <a href="javascript:void(0);" @click="scrollToSection('contact-us')">Contact Us</a>       
        <a href="javascript:void(0);" @click="scrollToSection('about-us')">About Us</a>
        <a href="javascript:void(0);" @click="goToPage('/create-account')">Sign up</a>
      </nav>
    </header>

    <section class="hero" id="home">
      <div class="hero-text">
        <h1>Enjoy Your Morning Coffee in UIC Café Beàta</h1>
        <p>Boost your productivity and build your mood with a glass of coffee in the morning.</p>
        <button class="get-now-btn" @click="goToPage('/login')">Get your Coffee now!</button>
        <button class="play-video-btn" @click="scrollToSection('contact-us')">Contact Us</button>
      </div>
      <div class="hero-image">
        <img src="@/assets/pink-cafe.png" alt="Coffee Cup" />
      </div>
    </section>

    <!-- About Us Section -->
    <section class="about-us" id="about-us">
      <h2>About Us</h2>
      <p>Welcome to the University of the Immaculate Conception Café Beàta, your go-to spot for delicious and affordable food on campus. Established in 2020, our café serves students, faculty, and staff, offering a variety of fresh and high-quality meals and beverages in a convenient setting.</p>
      <p>More than just a place to eat, our café is a hub for community engagement, where people come together to connect, relax, and recharge. We are committed to providing excellent service while promoting sustainability and customer satisfaction in everything we do.</p>
    </section>

    <!-- Footer Section (Now above Contact Us) -->
    <footer class="footer">
      <p>Enjoy your coffee in our comfortable place</p>
      <div class="footer-info">
        <div>
          <h4>14+</h4>
          <p>Study Table</p>
        </div>
        <div>
          <h4>10+</h4>
          <p>Drinks</p>
        </div>
        <div>
          <h4>9+</h4>
          <p>Food</p>
        </div>
      </div>
    </footer>

    <!-- Contact Us Section (Moved to the bottom) -->
    <section class="contact-us" id="contact-us">
      <h2>Contact Us</h2>
      <p>If you have any questions or want to get in touch, reach us on our social media platforms:</p>
      <div class="social-icons">
        <a href="https://www.facebook.com/profile.php?id=61573775720122" target="_blank" class="social-icon">
          <img src="@/assets/facebook-icon.png" alt="Facebook" />
        </a>
        <a href="https://www.instagram.com/uic_ph/?fbclid=IwY2xjawIn_-RleHRuA2FlbQIxMAABHUVRHCqq6hn_mB-xsRdZn0b1mPnLcMVcrlTYxrqWnMgYYR3zq-ObdYi_Rg_aem_WxzwcAo7_v633IXI50R6mQ#" target="_blank" class="social-icon">
          <img src="@/assets/instagram.png" alt="Instagram" />
        </a>
      </div>
    </section>
  </div>
</template>



<script>
export default {
  name: "CoffeePage",
  methods: {
    // Scrolls to the top of the page
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    // Scrolls to the specific section
    scrollToSection(sectionId) {
      const section = document.getElementById(sectionId);
      if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
      }
    },

    // Redirects to a different page
    goToPage(pageUrl) {
      this.$router.push(pageUrl);
    }
  }
};
</script>

<style scoped>
.coffee-container {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8d1d1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  top: 0;
  display: flex;
  justify-content: space-between;
  padding: 15px 20px; /* Adjusted for better mobile fit */
  background-color: #fce6e6;
  z-index: 1000; /* Ensures it stays above other content */
  position: sticky; 
  border-bottom: 2px solid #d88e8e; /* Added border for a more defined header */
}

.logo {
  font-size: 1.8em; /* Slightly smaller font size for better fit */
  font-weight: bold;
   font-family: 'Roboto', sans-serif;
  color:rgb(180, 102, 102); /* Highlight text color */
  margin-left: 10px;
  cursor: pointer; /* Make it clickable */
  text-transform: uppercase; /* Adds emphasis */
}

.nav-links {
  display: flex;
  gap: 20px;
  font-size: 1.1em; /* Slightly smaller font size */
  font-weight: bold;
   font-family: 'Roboto', sans-serif;
  color: #5e5e5e;
}

.nav-links a {
  text-decoration: none;
  color: #5e5e5e;
  transition: color 0.3s ease;
  cursor: pointer;
}

.nav-links a:hover {
  color: #f4a261;
  text-decoration: underline; /* Added underline effect on hover */
}

.hero {
  display: flex;
  justify-content: space-between;
  padding: 40px;
  background-color: #f8d1d1;
  flex-wrap: wrap;
}

.hero-text {
  max-width: 50%;
  padding: 20px;
}

.hero-text h1 {
  font-size: 3em;
  color: #3b2a2a;
}

.hero-text p {
  margin-top: 10px;
  font-size: 1.2em;
  color: #5e5e5e;
}

.get-now-btn,
.play-video-btn {
  background-color: #f4a261;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1em;
  cursor: pointer;
  margin-top: 20px;
  margin-right: 10px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.get-now-btn:hover,
.play-video-btn:hover {
  background-color: #e0763d;
}

.hero-image {
  max-width: 50%;
}

.hero-image img {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
}

/* About Us Section */
.about-us {
  background-color: #fce6e6;
  padding: 40px;
  text-align: center;
}

.about-us h2 {
  font-size: 2.5em;
  color: #3b2a2a;
}

.about-us p {
  font-size: 1em;
  color: #5e5e5e;
  max-width: 800px;
  margin: 0 auto;
}

/* Contact Us Section */
.contact-us {
  padding: 40px;
  text-align: center;
  background-color: #fce6e6;
}

.contact-us h2 {
  font-size: 2.5em;
  color: #3b2a2a;
}

.contact-us p {
  font-size: 1.2em;
  color: #5e5e5e;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.social-icon img {
  width: 40px;
  height: 40px;
  transition: transform 0.3s ease;
}

.social-icon img:hover {
  transform: scale(1.1);
}

/* Footer */
.footer {
  background-color: #f8d1d1;
  padding: 40px;
  text-align: center;
}

.footer-info {
  display: flex;
  justify-content: space-around;
  gap: 20px;
  flex-wrap: wrap;
}

.footer-info div {
  text-align: center;
}

.footer-info h4 {
  font-size: 2em;
  color: #3b2a2a;
}

.footer-info p {
  font-size: 1.2em;
  color: #5e5e5e;
}

/* Media Queries for responsiveness */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    padding: 15px 10px;
    align-items: center;
  }

  .logo {
    font-size: 1.6em;
    text-align: center;
  }

  .nav-links {
    flex-direction: column;
    gap: 10px;
    font-size: 1em;
  }

  .hero {
    flex-direction: column;
    padding: 20px;
  }

  .hero-text {
    max-width: 100%;
    text-align: center;
  }

  .hero-text h1 {
    font-size: 2.5em;
  }

  .hero-text p {
    font-size: 1em;
  }

  .hero-image {
    max-width: 100%;
    margin-top: 20px;
  }

  .footer-info {
    display: block;
  }

  .footer-info div {
    margin-bottom: 20px;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 10px 5px;
  }

  .logo {
    font-size: 1.9em;
  }

  .nav-links {
    flex-direction: column;
    gap: 8px;
    font-size: 1.1em;
  }

  .nav-links a {
    font-size: 1em;
    text-align: center;
      color:rgb(189, 56, 56);
  }

  .nav-links a:hover {
    color: #f4a261;
    text-decoration: underline;
  }

  .hero-text h1 {
    font-size: 2em;
  }

  .hero-text p {
    font-size: 0.9em;
  }

  .footer-info h4 {
    font-size: 1.5em;
  }

  .footer-info p {
    font-size: 1em;
  }

  .get-now-btn,
  .play-video-btn {
    width: 100%;
    margin-top: 10px;
  }
}
</style>
