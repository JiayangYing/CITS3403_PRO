const DefaultValueWhenNull = "-";

function setLogo() {
  $(".login-container .company-logo").replaceWith(
    `<span class="company-logo fa-stack fa-flip fa-4x">
            <span class="fa-layers fa-fw">
                <span class="logo-word pos-up">Eco</span>
                <span class="logo-word pos-down">HUB</span>
            </span>
            <i class="fa-solid fa-leaf fa-stack-1x"></i>
        </span>`
  );
}

function CallPost(url, data, callbackSuccess, callbackError) {
  window.$.ajax({
    type: "POST",
    contentType: "application/json",
    url: url,
    data: JSON.stringify(data),
    success: callbackSuccess,
    error: function (xhr, status, error) {
      callbackError?.(xhr, status, error);
    },
  });
}

const OnAjaxError = (xhr) => {
  var response;
  try {
    if (xhr.status && xhr.status === 404) {
      GenerateDangerAlertDiv(
        "Failed!",
        `ErrorCode: ${xhr.status}. The requested page cannot be found.`
      );
      return;
    }

    response = JSON.parse(xhr.responseText);

    if (response) {
      GenerateDangerAlertDiv("Failed!", response.message);
    }
  } catch (e) {
    GenerateDangerAlertDiv("Failed!", xhr.responseText);
  }
};

function GenerateSuccessAlertDiv(title, message, divId) {
  if (!divId) {
    divId = "#AlertModalDiv";
  }

  window
    .$(divId)
    .removeClass()
    .addClass("alert alert-success alert-dismissible");
  window.$(divId)
    .html(`<button type="button" class="close" aria-hidden="true" onclick="CloseAlertDiv('${divId}')">&times;</button>\n
                                <h4><i class="icon fa fa-check"></i>${title}</h4>\n
                                <span id="AlertMessage">${message}</span>`);
  ScrollToTopPage();
}

function GenerateInfoAlertDiv(title, message, divId) {
  if (!divId) {
    divId = "#AlertModalDiv";
  }

  window.$(divId).removeClass().addClass("alert alert-info alert-dismissible");
  window.$(divId)
    .html(`<button type="button" class="close" aria-hidden="true" onclick="CloseAlertDiv('${divId}')">&times;</button>\n
                                <h4><i class="icon fa fa-info-circle me-2"></i>${title}</h4>\n
                                <span id="AlertMessage">${message}</span>`);
  ScrollToTopPage();
}

function GenerateWarningAlertDiv(title, message, divId) {
  if (!divId) {
    divId = "#AlertModalDiv";
  }

  window
    .$(divId)
    .removeClass()
    .addClass("alert alert-warning alert-dismissible");
  window.$(divId)
    .html(`<button type="button" class="close" aria-hidden="true" onclick="CloseAlertDiv('${divId}')">&times;</button>\n
                                        <h4><i class="icon fa fa-exclamation-triangle"></i>${title}</h4>\n
                                        <span id="AlertMessage">${message}</span>`);
  ScrollToTopPage();
}

function GenerateDangerAlertDiv(title, message, divId) {
  if (!divId) {
    divId = "#AlertModalDiv";
  }

  window
    .$(divId)
    .removeClass()
    .addClass("alert alert-danger alert-dismissible");
  window.$(divId)
    .html(`<button type="button" class="close" aria-hidden="true" onclick="CloseAlertDiv('${divId}')">&times;</button>\n
                                    <h4><i class="icon fa fa-ban"></i>${title}</h4>\n
                                    <span id="AlertMessage">${message}</span>`);
  ScrollToTopPage();
}

function CloseAlertDiv(divId) {
  if (!divId) {
    divId = "#AlertModalDiv";
  }

  window.$(divId).addClass("d-none");
}

function ScrollToTopPage() {
  document.body.scrollTop = document.documentElement.scrollTop = 0;
}

function stringToBool(_str) {
  if (_str == null) {
    return false;
  }
  var str = _str.toLowerCase().trim();
  return str === "true" || str === "yes" || str === "1";
}

function SetPaginationActive(id) {
  var url = new URL(window.location.href);
  pageNum = url.searchParams.get("page");
  if (!pageNum) {
    $(`${id} :contains("1")`).parent().addClass("active");
  } else {
    $(`${id} a`).each(function (i, a) {
      $a = $(a);
      if (`${$a.text()}` === pageNum) {
        $a.parent().addClass("active");
        return false;
      }
    });
  }
}

const darkModeClass = "dark_mode";
$(() => {
  const lightSwitch = document.getElementById("toggleDarkTheme");
  const toggleSpan = lightSwitch.querySelector("i");
  const textSpan = lightSwitch.querySelector("span");
  setLogo();
  if (stringToBool(localStorage.getItem(darkModeClass))) {
    document.querySelector("body").classList.add(darkModeClass);
    toggleSpan.classList.replace("fa-moon", "fa-sun");
    textSpan.textContent = textSpan.dataset.light;
  }
});

function updateUrlParameter(key, value) {
  var url = new URL(window.location.href);
  url.searchParams.set(key, value);
  window.location.href = url.toString();
}
