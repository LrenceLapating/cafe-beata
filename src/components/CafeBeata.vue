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
      <p>Established in 2020, UIC Café Beata serves as a welcoming space for students, faculty, and staff at the University of the Immaculate Conception. Committed to providing high-quality and affordable food and beverages, our café has become a central hub for the campus community. With a focus on freshness, sustainability, and customer satisfaction, we strive to create a comfortable and engaging environment where everyone can connect and enjoy great food.</p>
    </section>

    <!-- Best Selling Item Section (Added Below About Us) -->
    <section class="best-selling" id="best-selling">
      <h2>Best Selling Item</h2>
      <p class="description">UIC Café Beata – Since 2020 Our top-selling item stands out for its exceptional quality and taste. Crafted with the finest ingredients, it has been a customer favorite since we first opened our doors. Experience the perfect blend of flavor and tradition with every bite.</p>
      
      <div class="filter-menu">
        <span class="active">All</span>
        <span>Black</span>
        <span>Espresso</span>
        <span>Doppio</span>
      </div>

      <div class="coffee-items">
        <div class="coffee-card">
          <div class="coffee-img-container">
            <img src="@/assets/cappuccino.png" alt="Cappuccino">
          </div>
          <h3>Cappuccino</h3>           
          <button class="order-now-btn" @click="goToPage('/login')">Order Now</button>
        </div>

        <div class="coffee-card">
          <div class="coffee-img-container">
            <img src="@/assets/americano.png" alt="Americano">
          </div>
          <h3>Americano</h3>
          <button class="order-now-btn" @click="goToPage('/login')">Order Now</button>
        </div>

        <div class="coffee-card">
          <div class="coffee-img-container">
            <img src="@/assets/espresso.png" alt="Espresso">
          </div>
          <h3>Espresso</h3>
          <button class="order-now-btn" @click="goToPage('/login')">Order Now</button>
        </div>
      </div>

      <div class="pagination">
        <button class="prev-btn">⬅</button>
        <button class="next-btn">➞</button>
      </div>
    </section>

    <!-- Contact Us Section (Updated Design) -->
    <section class="contact-us" id="contact-us">
      <div class="contact-header">
        <h2>Stay Up To Date On<br>All News And Offers.</h2>
        <p>Be The First To Know About New Collections, Special Events, And What’s Going On At UIC Café Beàta.</p>
        <div class="newsletter">
          <input type="email" placeholder="Enter Your Email Address">
          <button>➞</button>
        </div>
      </div>

      <div class="contact-content">
        <div class="contact-box">
          <h3 class="contact-title">UIC Café Beàta</h3>
          <p>Enjoy better and better quality coffee with UIC Café Beàta.</p>
        </div>

        <div class="contact-box">
          <h3 class="contact-title">Contact Us</h3>
          <p>Email: cafebeatauic@gmail.com</p>
          <p>Call Us: (321) 562 – 57420</p>
          <p>Text Us: (321) 562 – 57420</p>
          <p>Fr Selga, Davao City, Philippines</p>
        </div>

        <div class="contact-box">
          <h3 class="contact-title">Follow Us</h3>
          <div class="social-icons">
            <a href="https://www.facebook.com/profile.php?id=61573775720122" target="_blank">
              <img src="@/assets/facebook-icon.png" alt="Facebook">
            </a>
            <a href="https://www.instagram.com/uic_ph/" target="_blank">
              <img src="@/assets/instagram.png" alt="Instagram">
            </a>
          </div>
        </div>
      </div>

      <p class="copyright">Copyright: 2023 UIC Café Beàta</p>
    </section>
  </div>
</template>



<script>
export default {
  name: "CoffeePage",
  methods: {
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    scrollToSection(sectionId) {
      const section = document.getElementById(sectionId);
      if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
      }
    },
    goToPage(pageUrl) {
      this.$router.push(pageUrl);
    }
  }
};
</script>


<style scoped>

/* Mobile Responsive Adjustments */
@media (max-width: 768px) {
  .best-selling {
    padding: 30px;
  }

  .best-selling h2 {
    font-size: 2em;
  }

  .description {
    font-size: 1em;
    max-width: 100%;
    padding: 0 10px;
  }

  .filter-menu {
    flex-wrap: wrap;
    gap: 10px;
    font-size: 1em;
  }

  .coffee-items {
    flex-direction: column;
    align-items: center;
  }

  .coffee-card {
    max-width: 200px;
    padding: 10px;
  }

  .coffee-card img {
    width: 100px;
    height: 100px;
  }

  .coffee-card h3 {
    font-size: 1.2em;
  }

  .coffee-card button {
    font-size: 0.9em;
    padding: 8px;
  }

  .pagination {
    margin-top: 15px;
  }

  .pagination button {
    font-size: 1em;
    padding: 6px 12px;
  }
}

@media (max-width: 480px) {
  .best-selling {
    padding: 20px;
  }

 

  .filter-menu {
    flex-direction: column;
    text-align: center;
    gap: 8px;
  }

  .coffee-card {
    max-width: 180px;
    padding: 8px;
  }

  .coffee-card img {
    width: 80px;
    height: 80px;
  }

  .coffee-card h3 {
    font-size: 1em;
  }

  .coffee-card button {
    font-size: 0.8em;
    padding: 6px;
  }

  .pagination button {
    font-size: 0.9em;
    padding: 5px 10px;
  }
}


/* Best Selling Section */
.best-selling {
      background-color:rgb(233, 177, 177);
  padding: 50px;
  text-align: center;
  border-radius: 15px;
  margin: 40px auto;
  max-width: 1000px;
}

.best-selling h2 {
  font-size: 2.5em;
  color: #3b2a2a;
}



.filter-menu {
  display: flex;
  justify-content: center;
  gap: 20px;
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 30px;
}

.filter-menu span {
  cursor: pointer;
  padding: 5px 10px;
}

.filter-menu .active {
  text-decoration: underline;
}

.coffee-items {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.coffee-card {
  background-color: #332621;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  max-width: 250px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  border: 4px solid black;
}

.coffee-img-container {
  background-color: #f5f5f5;
  padding: 5px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.coffee-card img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 5px;
}

.coffee-card h3 {
  font-size: 1.5em;
  color: white;
  font-weight: bold;
}

.coffee-card button {
  background-color: #d2a679;
  color: black;
  border: none;
  padding: 10px;
  font-size: 1em;
  cursor: pointer;
  margin-top: 10px;
  border-radius: 5px;
  width: 100%;
  font-weight: bold;
}

.coffee-card button:hover {
  background-color: #b4845c;
}

.pagination {
  margin-top: 20px;
}

.pagination button {
  background-color: black;
  color: white;
  border: none;
  padding: 8px 15px;
  font-size: 1.2em;
  cursor: pointer;
  margin: 5px;
  border-radius: 5px;
}

.pagination button:hover {
  background-color: #444;
}

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
  animation: slideIn 0.5s ease-out; /* Header slide-in animation */
}

.logo {
  font-size: 1.8em; /* Slightly smaller font size for better fit */
  font-weight: bold;
  font-family: 'Roboto', sans-serif;
  color: rgb(180, 102, 102); /* Highlight text color */
  margin-left: 10px;
  cursor: pointer; /* Make it clickable */
  text-transform: uppercase; /* Adds emphasis */
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.1); /* Logo scaling on hover */
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
  transition: color 0.3s ease, transform 0.3s ease;
  cursor: pointer;
}

.nav-links a:hover {
  color: #f4a261;
  text-decoration: underline;
  transform: scale(1.1); /* Hover scaling for links */
}

.hero {
  display: flex;
  justify-content: space-between;
  padding: 40px;
  background: linear-gradient(to right, #f8d1d1, #fce6e6);
  flex-wrap: wrap;
  animation: fadeIn 1s ease-in-out; /* Fade-in animation for hero section */
}

.hero-text {
  max-width: 50%;
  padding: 20px;
  animation: slideInRight 1s ease-out; /* Slide-in right animation */
}

.hero-text h1 {
  font-size: 3em;
  color: #3b2a2a;
  animation: fadeIn 1s ease-in-out;
}

.hero-text p {
  margin-top: 10px;
  font-size: 1.2em;
  color: #5e5e5e;
  animation: fadeIn 1s ease-in-out 0.5s; /* Delay for paragraph */
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
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Box shadow */
}

.get-now-btn:hover,
.play-video-btn:hover {
  background-color: #e0763d;
  transform: scale(1.05); /* Button scaling effect */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Hover box shadow */
}

.hero-image {
  max-width: 50%;
}

.hero-image img {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  animation: fadeIn 1s ease-in-out 0.8s; /* Fade-in with delay */
  transition: transform 0.3s ease;
}

.hero-image img:hover {
  transform: scale(1.05); /* Slight zoom on hover */
}

/* About Us Section */
.about-us {
  background-color: #fce6e6;
  padding: 40px;
  text-align: center;
  animation: fadeIn 1s ease-in-out 1s; /* About section fade-in */
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1); /* Card-like shadow */
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
  background-color: #fce6e6;
  color: white;
  padding: 50px 20px;
  text-align: center;

.contact-header h2 {
  font-size: 2.5em;
  font-weight: bold;
}

.contact-header p {
  font-size: 1em;
  margin-bottom: 20px;
}

.newsletter {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.newsletter input {
  width: 300px;
  padding: 10px;
  font-size: 1em;
  border: none;
  outline: none;
}

.newsletter button {
  background-color: black;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1.2em;
}

.contact-content {
  display: flex;
  justify-content: space-around;
  margin-top: 40px;
  flex-wrap: wrap;
}


.contact-box {
  background-color: #f8d1d1;
  padding: 3px;
  border-radius: 10px;
  width: 300px;
  text-align: center;
  margin-bottom: 20px;
}

.contact-title {
  font-size: 1.5em;
  font-weight: bold;
  color: black;
}

.contact-box p {
  font-size: 1em;
  margin: 10px 0;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.social-icons a img {
  width: 30px;
  height: 30px;
  transition: transform 0.3s ease;
}

.social-icons a img:hover {
  transform: scale(1.1);
}

.copyright {
  margin-top: 30px;
  font-size: 0.9em;
  opacity: 0.8;
}

/* Responsive Design */
@media (max-width: 768px) {
  .contact-header h2 {
    font-size: 2em;
  }

  .contact-content {
    flex-direction: column;
    align-items: center;
  }

  .contact-box {
    width: 80%;
  }

  .newsletter input {
    width: 250px;
  }
}

@media (max-width: 480px) {
  .contact-header h2 {
    font-size: 1.8em;
  }

  .newsletter input {
    width: 200px;
  }

  .contact-box {
    width: 100%;
  }

  .social-icons a img {
    width: 25px;
    height: 25px;
  }
}



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
  transition: transform 0.3s ease, filter 0.3s ease;
}

.social-icon img:hover {
  transform: scale(1.1);
  filter: brightness(1.3); /* Brighten on hover */
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

/* Animations */
@keyframes slideIn {
  0% {
    transform: translateY(-100%);
  }
  100% {
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes slideInRight {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(0);
  }
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
    color: rgb(189, 56, 56);
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