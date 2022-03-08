static char *text_html = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
static char *text_htm = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
static char *text_css = "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n";
static char *image_jpeg = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n";
static char *text_plain = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
static char *image_gif = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n";
static char *application_xml = "HTTP/1.1 200 OK\r\nContent-Type: application/xml\r\n\r\n";
static char *application_json = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n";

static char *bad_request = "HTTP/1.1 404 File not found\n\n";
static char *unsupported_type = "HTTP/1.1 415 Unsupported Media Type\n\n";