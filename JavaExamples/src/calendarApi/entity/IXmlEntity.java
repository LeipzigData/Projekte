package calendarApi.entity;

import org.w3c.dom.Node;

/**
 * Simple interface for XML serialization/deserialization.
 * 
 * @author Christof Pieloth
 * 
 * @param <ENTITY>
 *            Type which to serialization/deserialization
 */
public interface IXmlEntity<ENTITY> {

	/**
	 * Entity ID, if object could not be parsed.
	 */
	public static final String EMPTY_ID = "-1";

	/**
	 * Fills the object with the data from a XML element.
	 * 
	 * @param element
	 *            XML node for this Object
	 * @return this
	 */
	public ENTITY fromXml(Node element);

	/**
	 * Serializes this object to its XML representation.
	 * 
	 * @return XML node
	 */
	public Node toXml();
}
