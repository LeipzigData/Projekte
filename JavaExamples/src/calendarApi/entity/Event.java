package calendarApi.entity;

import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import com.sun.istack.internal.logging.Logger;

/**
 * An object for Event data.
 * 
 * @author Christof Pieloth
 * 
 */
public class Event implements IXmlEntity<Event> {
	private static final Logger jlog = Logger.getLogger(Event.class);

	// Attributes for XML
	private static final String EVENT_ID = "id";
	private static final String EVENT_NAME = "name";
	private static final String EVENT_DESCRIPTION = "description";
	private static final String EVENT_VENUEID = "venue-id";
	private static final String EVENT_SDATE = "date-from";
	private static final String EVENT_STIME = "time-from";
	private static final String EVENT_EDATE = "date-to";
	private static final String EVENT_ETIME = "time-time";

	private String id = EMPTY_ID;
	private String name;
	private String description;

	private String dateFrom;
	private String timeFrom;

	private String dateTo;
	private String timeTo;

	private String venueId;

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String getDateFrom() {
		return dateFrom;
	}

	public void setDateFrom(String dateFrom) {
		this.dateFrom = dateFrom;
	}

	public String getTimeFrom() {
		return timeFrom;
	}

	public void setTimeFrom(String timeFrom) {
		this.timeFrom = timeFrom;
	}

	public String getDateTo() {
		return dateTo;
	}

	public void setDateTo(String dateTo) {
		this.dateTo = dateTo;
	}

	public String getTimeTo() {
		return timeTo;
	}

	public void setTimeTo(String timeTo) {
		this.timeTo = timeTo;
	}

	public String getVenueId() {
		return venueId;
	}

	public void setVenueId(String venueId) {
		this.venueId = venueId;
	}

	@Override
	public Event fromXml(Node element) {
		if (element == null) {
			this.setId(EMPTY_ID);
			jlog.severe("Can not parse empty node!");
		}

		NodeList nodes = element.getChildNodes();
		for (int i = 0; i < nodes.getLength(); ++i) {
			final Node node = nodes.item(i);
			final String name = node.getNodeName();

			if (EVENT_ID.equals(name)) {
				this.setId(node.getTextContent());
			} else if (EVENT_NAME.equals(name)) {
				this.setName(node.getTextContent());
			} else if (EVENT_DESCRIPTION.equals(name)) {
				this.setDescription(node.getTextContent());
			} else if (EVENT_SDATE.equals(name)) {
				this.setDateFrom(node.getTextContent());
			} else if (EVENT_STIME.equals(name)) {
				this.setTimeFrom(node.getTextContent());
			} else if (EVENT_EDATE.equals(name)) {
				this.setDateTo(node.getTextContent());
			} else if (EVENT_ETIME.equals(name)) {
				this.setTimeTo(node.getTextContent());
			} else if (EVENT_VENUEID.equals(name)) {
				this.setVenueId(node.getTextContent());
			}
		}
		return this;
	}

	@Override
	public Node toXml() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String toString() {
		final StringBuilder sb = new StringBuilder();
		sb.append("ID: ").append(getId()).append("\n");
		sb.append("Name: ").append(getName()).append("\n");
		sb.append("Venue ID: ").append(getVenueId()).append("\n");
		sb.append("Date from: ").append(getDateFrom()).append("\n");
		sb.append("Time from: ").append(getTimeFrom()).append("\n");
		sb.append("Date to: ").append(getDateTo()).append("\n");
		sb.append("Time to: ").append(getTimeTo()).append("\n");
		sb.append("Desciption: ").append(getDescription());
		return sb.toString();
	}

}
