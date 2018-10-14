package calendarApi.entity;

import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import com.sun.istack.internal.logging.Logger;

/**
 * A object for Venue data.
 * 
 * @author Christof Pieloth
 * 
 */
public class Venue implements IXmlEntity<Venue> {
	private static final Logger jlog = Logger.getLogger(Venue.class);

	// Attributes for XML
	private static final String VENUE_ID = "id";
	private static final String VENUE_NAME = "name";
	private static final String VENUE_CITY = "city";
	private static final String VENUE_STREET = "street";
	private static final String VENUE_STREETNB = "housenumber";
	private static final String VENUE_POSTCODE = "postcode";
	private static final String VENUE_DESCRIPTION = "description";

	private String id = EMPTY_ID;
	private String name;
	private String description;
	private String street;
	private String housenumber;
	private String postcode;
	private String city;

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

	public String getStreet() {
		return street;
	}

	public void setStreet(String street) {
		this.street = street;
	}

	public String getHousenumber() {
		return housenumber;
	}

	public void setHousenumber(String housenumber) {
		this.housenumber = housenumber;
	}

	public String getPostcode() {
		return postcode;
	}

	public void setPostcode(String postcode) {
		this.postcode = postcode;
	}

	public String getCity() {
		return city;
	}

	public void setCity(String city) {
		this.city = city;
	}

	@Override
	public Venue fromXml(Node element) {
		if (element == null) {
			this.setId(EMPTY_ID);
			jlog.severe("Can not parse empty node!");
		}

		NodeList nodes = element.getChildNodes();
		for (int i = 0; i < nodes.getLength(); ++i) {
			final Node node = nodes.item(i);
			final String name = node.getNodeName();

			if (VENUE_ID.equals(name)) {
				this.setId(node.getTextContent());
			} else if (VENUE_NAME.equals(name)) {
				this.setName(node.getTextContent());
			} else if (VENUE_DESCRIPTION.equals(name)) {
				this.setDescription(node.getTextContent());
			} else if (VENUE_STREET.equals(name)) {
				this.setStreet(node.getTextContent());
			} else if (VENUE_STREETNB.equals(name)) {
				this.setHousenumber(node.getTextContent());
			} else if (VENUE_POSTCODE.equals(name)) {
				this.setPostcode(node.getTextContent());
			} else if (VENUE_CITY.equals(name)) {
				this.setCity(node.getTextContent());
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
		sb.append("Street: ").append(getStreet()).append("\n");
		sb.append("Housenumber: ").append(getHousenumber()).append("\n");
		sb.append("Postcode: ").append(getPostcode()).append("\n");
		sb.append("City: ").append(getCity()).append("\n");
		sb.append("Description: ").append(getDescription());
		return sb.toString();
	}

}
