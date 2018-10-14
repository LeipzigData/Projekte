package calendarApi.api;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import calendarApi.entity.Event;
import calendarApi.entity.Venue;

import com.sun.istack.internal.logging.Logger;

/**
 * Base implementation of Calendar API of API.Leipzig. This class can be used
 * for each webservice which has a "API.LEIPZIG-like" API.
 * 
 * @author Christof Pieloth
 * 
 */
public abstract class CalendarApi {

	private static final String LIST_NODE = "datum";

	private static final String DETAIL_NODE = "model";

	private final String key;
	public static final String DEFAULT_KEY = "unknown";

	private static final Logger jlog = Logger.getLogger(CalendarApi.class);

	public CalendarApi(String key) {
		this.key = key;
	}

	/**
	 * Gets the URL of the service which is used.
	 * 
	 * @return URL of service
	 */
	public abstract String getUrl();

	/**
	 * Gets the name of the service which is used.
	 * 
	 * @return Name of service
	 */
	public abstract String getName();

	/**
	 * Fetchs all events from <URL>/calendar/events
	 * 
	 * @return list of events or null
	 */
	public List<Event> getEvents() {
		final String strUrl = getUrl() + "/calendar/events";
		String document = getDocument(strUrl);

		if (document != null) {
			document = fixXml(document);
			
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory
					.newInstance();
			try {
				DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
				Document doc = dBuilder.parse(new ByteArrayInputStream(document
						.getBytes()));

				List<Event> events = new LinkedList<Event>();
				NodeList nodes = doc.getElementsByTagName(LIST_NODE);
				for (int i = 0; i < nodes.getLength(); ++i) {
					final Node node = nodes.item(i);
					final Event event = new Event();
					events.add(event.fromXml(node));
				}

				return events;
			} catch (ParserConfigurationException e) {
				jlog.severe(e.getMessage(), e);
			} catch (SAXException e) {
				jlog.severe(e.getMessage(), e);
			} catch (IOException e) {
				jlog.severe(e.getMessage(), e);

			}
		} else {
			jlog.severe("No document to parse!");
		}
		return null;
	}

	/**
	 * Fetchs an event from <URL>/calendar/events/<id>
	 * 
	 * @param id
	 *            Event ID
	 * @return Event or null
	 */
	public Event getEvent(String id) {
		final String strUrl = getUrl() + "/calendar/events/" + id;
		String document = getDocument(strUrl);

		if (document != null) {
			document = fixXml(document);
			
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory
					.newInstance();
			try {
				DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
				Document doc = dBuilder.parse(new ByteArrayInputStream(document
						.getBytes()));

				NodeList nodes = doc.getElementsByTagName(DETAIL_NODE);
				if (nodes.getLength() == 1) {
					final Node node = nodes.item(0);
					final Event event = new Event();
					return event.fromXml(node);
				} else {
					jlog.severe("None or to many nodes!");
				}
			} catch (ParserConfigurationException e) {
				jlog.severe(e.getMessage(), e);
			} catch (SAXException e) {
				jlog.severe(e.getMessage(), e);
			} catch (IOException e) {
				jlog.severe(e.getMessage(), e);
			}
		} else {
			jlog.severe("No document to parse!");
		}
		return null;
	}

	/**
	 * Fetchs a venue from <URL>/calendar/venues/<id>
	 * 
	 * @param id
	 *            Venue ID
	 * @return Venue or null
	 */
	public Venue getVenue(String id) {
		final String strUrl = getUrl() + "/calendar/venues/" + id;
		String document = getDocument(strUrl);

		if (document != null) {
			document = fixXml(document);
			
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory
					.newInstance();
			try {
				DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
				Document doc = dBuilder.parse(new ByteArrayInputStream(document
						.getBytes()));

				NodeList nodes = doc.getElementsByTagName(DETAIL_NODE);
				if (nodes.getLength() == 1) {
					final Node node = nodes.item(0);
					final Venue venue = new Venue();
					return venue.fromXml(node);
				} else {
					jlog.severe("None or to many nodes!");
				}
			} catch (ParserConfigurationException e) {
				jlog.severe(e.getMessage(), e);
			} catch (SAXException e) {
				jlog.severe(e.getMessage(), e);
			} catch (IOException e) {
				jlog.severe(e.getMessage(), e);
			}
		} else {
			jlog.severe("No document to parse!");
		}
		return null;
	}

	/**
	 * Requests the content from the service.
	 * 
	 * @param strUrl
	 *            URL for request
	 * @return Document or null
	 */
	protected String getDocument(String strUrl) {
		strUrl += "?api_key=" + key + "&format=xml";

		StringBuilder sb = new StringBuilder();
		HttpURLConnection con = null;
		Scanner scanner = null;
		try {
			URL url = new URL(strUrl);
			con = (HttpURLConnection) url.openConnection();
			if (con.getResponseCode() >= 400) {
				throw new Exception("Unknown HTTP error!");
			}

			scanner = new Scanner(con.getInputStream());
			while (scanner.hasNext())
				sb.append(scanner.next());
		} catch (MalformedURLException e) {
			jlog.severe("Could not create URL!", e);
			return null;
		} catch (IOException e) {
			jlog.severe(e.getMessage(), e);
			return null;
		} catch (Exception e) {
			jlog.severe(e.getMessage(), e);
			return null;
		} finally {
			if (con != null)
				con.disconnect();
			if (scanner != null)
				scanner.close();
		}
		return sb.toString();
	}

	/**
	 * Replace wrong(?) nil= attributes.
	 * 
	 * @param document
	 * @return Document without wrong(?) attributes
	 */
	protected String fixXml(String document) {
		// TODO(cpieloth): Bug or feature?
		// e.g. document = document.replace("urlnil=\"true\"", "url");
		document = document.replace("nil=", " nil=");
		return document;
	}
}
