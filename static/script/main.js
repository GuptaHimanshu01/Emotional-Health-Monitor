
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    if (!header.classList.contains('header-scrolled')) {
      offset -= 10
    }

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Clients Slider
   */
//himan modifications

  function fetchEmployeesByHappinessIndex(happinessIndex) {
    fetch('http://127.0.0.1:5000/employees')
      .then(response => response.json())
      .then(data => {
        const filteredData = data.filter(emp => emp.HAPPINESS_INDEX === happinessIndex);
        updateTable(filteredData);
      })
      .catch(error => console.log(error));
  }

  function updateTable(result) {
    const tableBody = document.querySelector('#result-table tbody');
    tableBody.innerHTML = '';

    if (result.length === 0) {
      const row = document.createElement('tr');
      const col = document.createElement('td');
      col.setAttribute('colspan', '6');
      col.textContent = 'No records found';
      row.appendChild(col);
      tableBody.appendChild(row);
      return;
    }

    for (let i = 0; i < result.length; i++) {
      const row = document.createElement('tr');
      const empIdCol = document.createElement('td');
      empIdCol.textContent = result[i].EMP_ID;
      row.appendChild(empIdCol);
      const empNameCol = document.createElement('td');
      empNameCol.textContent = result[i].EMP_NAME;
      row.appendChild(empNameCol);
      const empEmailCol = document.createElement('td');
      empEmailCol.textContent = result[i].EMP_EMAIL;
      row.appendChild(empEmailCol);
      const projNameCol = document.createElement('td');
      projNameCol.textContent = result[i].PROJECT_NAME;
      row.appendChild(projNameCol);
      const locCol = document.createElement('td');
      locCol.textContent = result[i].LOCATION;
      row.appendChild(locCol);
      const mgrNameCol = document.createElement('td');
      mgrNameCol.textContent = result[i].MANAGER_NAME;
      row.appendChild(mgrNameCol);
      tableBody.appendChild(row);
    }
  }
  

  


  // Add event listeners to the emotion cards

  const happyBtn = document.querySelector('.emotion-card:nth-child(1)');
  happyBtn.addEventListener('click', () => {
    fetchEmployeesByHappinessIndex("8.00");
    const resultTableContainer = document.querySelector('#result-table-container');
    resultTableContainer.style.display = 'block';
});
  
  const sadBtn = document.querySelector('.emotion-card:nth-child(2)');
  sadBtn.addEventListener('click', () => {
    fetchEmployeesByHappinessIndex("6.00");
    const resultTableContainer = document.querySelector('#result-table-container');
    resultTableContainer.style.display = 'block';
  });
  
  const stressedBtn = document.querySelector('.emotion-card:nth-child(3)');
  stressedBtn.addEventListener('click', () => {
    fetchEmployeesByHappinessIndex("4.00");
    const resultTableContainer = document.querySelector('#result-table-container');
    resultTableContainer.style.display = 'block';
  });

  const disgustBtn = document.querySelector('.emotion-card:nth-child(4)');
  disgustBtn.addEventListener('click', () => {
    fetchEmployeesByHappinessIndex("2.00");
    const resultTableContainer = document.querySelector('#result-table-container');
    resultTableContainer.style.display = 'block';
  });
  
  const angryBtn = document.querySelector('.emotion-card:nth-child(5)');
  angryBtn.addEventListener('click', () => {
    fetchEmployeesByHappinessIndex("0.50");
    const resultTableContainer = document.querySelector('#result-table-container');
    resultTableContainer.style.display = 'block';
  });




  const hideTableBtn = document.querySelector('#hide-table-btn');
hideTableBtn.addEventListener('click', () => {
  const resultTableContainer = document.querySelector('#result-table-container');
  resultTableContainer.style.display = 'none';
});





//cards end


//search and chart script




  
      // Pie chart
      window.onload = function() {
        fetch('http://127.0.0.1:5000/employees/piechartdetails')
          .then(response => response.json())
          .then(data => {
            const chart_scores = data[0];
            const happy = parseFloat(chart_scores.happy), sadness = parseFloat(chart_scores.sadness), neutral = parseFloat(chart_scores.neutral), stressed = parseFloat(chart_scores.stressed), angry  = parseFloat(chart_scores.angry);
            const pieChart = new CanvasJS.Chart("pieChartContainer", {
              theme: "light2",
              exportEnabled: true,
              animationEnabled: true,
              title: {
                text: "Overall Emotion Count of Persistent Systems"
              },
              data: [{
                type: "pie",
                startAngle: 25,
                toolTipContent: "<b>{label}</b>: {y}%",
                showInLegend: "true",
                legendText: "{label}",
                indexLabelFontSize: 16,
                indexLabel: "{label} - {y}%",
                dataPoints: [
                  { y: happy, label: "Happy" },
                  { y: sadness, label: "Sad" },
                  { y: neutral, label: "Neutral" },
                  { y: angry, label: "Angry" },
                  { y: stressed, label: "Stressed" },
                ]
              }]
            });
            pieChart.render();
          });
      };
    
      // Bar chart
      fetch('http://127.0.0.1:5000//employees/barchartdetails')
        .then(response => response.json())
        .then(data => {
          const chart_data = data[0];
          const ctx = document.getElementById('barChart').getContext('2d');
          const barChart = new Chart(ctx, {
            type: 'bar',
            
            data: {
              labels: ['Pune', 'Indore', 'Nagpur', 'Hyderabad', 'Goa', 'Banglore'],
              datasets: [{
                label: 'Percentage',
                data: [chart_data.pune, chart_data.indore, chart_data.nagpur, chart_data.hyderabad, chart_data.goa, chart_data.banglore],
                backgroundColor: '#3e95cd',
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              scales: {
                yAxes: [{
                  ticks: {
                    beginAtZero: true
                  }
                }]
              },
              title: {
                display: true,
                text: 'Emotion Distribution by City'
              }
            }
          });
        })
        .catch(error => {
          console.log(error);
        });
  



  /**
   * Animation on scroll
   */
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: "ease-in-out",
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', () => {
    aos_init();
  });

  /**
   * Initiate Pure Counter 
   */
  new PureCounter();






})();



